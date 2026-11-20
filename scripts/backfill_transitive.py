import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def backfill():
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

        # Format: (prefix_text, subject_tag, object_tag, color)
        prefix_map = {
            "ke": ("1sg", "3m/i", "Red"),
            "hse": ("2sg", "3m/i", "Red"),
            "ra": ("3m", "3m/i", "Blue"),
            "ye": ("3f", "3m/i", "Blue"),
            "ka": ("3i", "3m/i", "Blue"),
            "wake": ("3m/i", "1sg", "Blue"),
            "kon": ("1sg", "2sg", "Purple"),
            "katate": ("1sg", "1sg", "Red"),
            "teyakyatate": ("1pl.in", "1pl.in", "Blue"),
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
                    subject_tag, object_tag, color = prefix_map[best_prefix]
                    vf.subject = subject_tag
                    vf.object = object_tag if object_tag != "3m/i" else None  # None = intransitive "it"
                    
                    p_morph = get_morph(best_prefix, "prefix", f"{subject_tag}_to_{object_tag}", color, f"{subject_tag} > {object_tag}")
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p_morph.id, sequence_order=1))
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_m.id, sequence_order=2))
                else:
                    # Just root
                    db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_m.id, sequence_order=1))
            
            db.session.commit()
            print(f"Backfilled traces for {vd['root']}")

if __name__ == "__main__":
    backfill()
