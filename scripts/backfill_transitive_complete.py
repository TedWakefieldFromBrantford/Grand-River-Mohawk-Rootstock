import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def backfill_complete():
    app = create_app()
    with app.app_context():
        def get_morph(text, m_type, func, color, label):
            m = Morpheme.query.filter_by(text=text, type=m_type, grammatical_function=func).first()
            if not m:
                m = Morpheme(text=text, type=m_type, grammatical_function=func, color_code=color, ui_label=label)
                db.session.add(m)
                db.session.commit()
            return m

        verbs_data = [
            {"root": "-nòn:we's", "root_text": "nòn:we's", "gloss": "like"},
            {"root": "-yenté:ri", "root_text": "yenté:ri", "gloss": "know"},
            {"root": "-norónhkwa", "root_text": "norónhkwa", "gloss": "love"},
            {"root": "-hswenhs", "root_text": "hswenhs", "gloss": "hate"},
        ]

        # ==========================================
        # THE COMPLETE PREFIX MAP
        # ==========================================
        prefix_map = {
            # --- Intransitive (Subject -> It) ---
            "ke":      ("1sg", None, "Red", False),
            "hse":     ("2sg", None, "Red", False),
            "ra":      ("3m", None, "Blue", False),
            "ye":      ("3f", None, "Blue", False),
            "ka":      ("3i", None, "Blue", False),
            "teni":    ("1du.ex", None, "Red", False),
            "yakeni":  ("1du.in", None, "Red", False),
            "seni":    ("2du", None, "Red", False),
            "hni":     ("2du.m", None, "Blue", False),
            "keni":    ("2du.f", None, "Blue", False),
            "tewa":    ("1pl.ex", None, "Red", False),
            "yakwa":   ("1pl.in", None, "Red", False),
            "sewa":    ("2pl", None, "Red", False),
            "rati":    ("3pl.m", None, "Blue", False),
            "konti":   ("3pl.f", None, "Blue", False),
            
            # --- Transitive (Subject -> Object) ---
            "wake":    ("3m/i", "1sg", "Blue", False),   # it -> me
            "kon":     ("1sg", "2sg", "Purple", False),  # I -> you
            "riyen":   ("1sg", "3m", "Purple", False),   # I -> him
            "kheyen":  ("1sg", "3f", "Purple", False),   # I -> her
            "take":    ("2sg", "1sg", "Purple", False),  # you -> me
            "takeni":  ("2du", "1sg", "Purple", False),  # you two -> me
            "takwa":   ("2pl", "1sg", "Purple", False),  # you all -> me
            "yesayen": ("3pl.m", "2sg", "Purple", False),# they -> you
            "ronwa":   ("3pl.m", "1pl", "Purple", False),# they -> us
            "yontati": ("3pl.f", "1sg", "Purple", False),# they Fs -> me

            # --- Reflexive/Reciprocal ---
            "katate":  ("1sg", "1sg", "Red", True),
            "hsatate": ("2sg", "2sg", "Red", True),
            "ratate":  ("3m", "3m", "Blue", True),
            "yontate": ("3f", "3f", "Blue", True),
            "watate":  ("3i", "3i", "Blue", True),
            "tyatate": ("1du", "1du", "Red", True),
            "yakyatate": ("1du", "1du", "Red", True),
            "tsyatate": ("2du", "2du", "Red", True),
            "hyatate": ("2du", "2du", "Blue", True),
            "kyatate": ("2du", "2du", "Blue", True),
            "tewatate": ("1pl", "1pl", "Red", True),
            "yakwatate": ("1pl", "1pl", "Red", True),
            "sewatate": ("2pl", "2pl", "Red", True),
            "rontate": ("3pl", "3pl", "Blue", True),
            "kontate": ("3pl", "3pl", "Blue", True),

            # --- Reciprocal ---
            "teyakyatate": ("1pl", "1pl", "Blue", True),
            "teyakyatateni": ("1du", "1du", "Blue", True),
        }

        for vd in verbs_data:
            verb = Verb.query.filter_by(root=vd["root"]).first()
            if not verb: continue
            
            root_m = get_morph(vd["root_text"], "root", f"{vd['gloss']}_root", None, f"Root: {vd['gloss']}")

            forms = VocabForm.query.filter_by(verb_id=verb.id).all()
            for vf in forms:
                FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
                
                # Find the best matching prefix (longest match first)
                best_prefix = None
                for prefix in sorted(prefix_map.keys(), key=len, reverse=True):
                    if vf.form.startswith(prefix):
                        best_prefix = prefix
                        break
                
                if best_prefix:
                    subject_tag, object_tag, color, is_reflexive = prefix_map[best_prefix]
                    vf.subject = subject_tag
                    vf.object = object_tag
                    
                    func = f"{subject_tag}_to_{object_tag if object_tag else '3m/i'}"
                    label = f"{subject_tag} > {object_tag if object_tag else 'it'}"
                    if is_reflexive:
                        label += " (Reflexive)" if subject_tag == object_tag else " (Reciprocal)"
                    
                    p_morph = get_morph(best_prefix, "prefix", func, color, label)
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p_morph.id, sequence_order=1))
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_m.id, sequence_order=2))
                else:
                    # Fallback if no prefix matches (shouldn't happen, but safety first)
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_m.id, sequence_order=1))
            
            db.session.commit()
            print(f"Backfilled traces for {vd['root']}")

if __name__ == "__main__":
    backfill_complete()
