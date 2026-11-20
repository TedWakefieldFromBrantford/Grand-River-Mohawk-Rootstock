import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def seed_morphemes():
    app = create_app()
    with app.app_context():
        def get_morph(text, m_type, func, color, label):
            m = Morpheme.query.filter_by(text=text, type=m_type).first()
            if not m:
                m = Morpheme(text=text, type=m_type, grammatical_function=func, 
                             color_code=color, ui_label=label)
                db.session.add(m)
                db.session.commit()
            return m

        # ==========================================
        # A-STEM: -atketskw (Page 157)
        # ==========================================
        verb_a = Verb.query.filter_by(root="-atketskw").first()
        root_a = get_morph("-atketskw-", "root", "get_up", None, "Root: Get Up")
        
        # Habitual Suffix
        hab_a_suffix = get_morph("-as", "suffix", "habitual_marker", None, "Habitual Suffix")
        # Perfective Suffix
        perf_a_suffix = get_morph("-en", "suffix", "perfective_marker", None, "Perfective Suffix")

        a_prefixes = {
            "habitual": {
                "1sg": ("k", "1sg_habitual_A", "Red"),
                "2sg": ("s", "2sg_habitual_A", "Red"),
                "3m/i": ("rat", "3m_habitual_A", "Blue"),
                "3f": ("yont", "3f_habitual_A", "Blue"),
            },
            "perfective": {
                "1sg": ("waka", "1sg_perfective_A", "Purple"),
                "2sg": ("sa", "2sg_perfective_A", "Purple"),
                "3m/i": ("rot", "3m_perfective_A", "Purple"),
                "3f": ("yakot", "3f_perfective_A", "Purple"),
            }
        }

        for aspect, subjects in a_prefixes.items():
            for subject, (prefix_text, func, color) in subjects.items():
                vf = VocabForm.query.filter_by(verb_id=verb_a.id, form_type=aspect, subject=subject).first()
                if not vf: continue
                
                # Clear existing trace
                FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
                
                p_morph = get_morph(prefix_text, "prefix", func, color, f"{subject} {aspect}")
                suffix = hab_a_suffix if aspect == "habitual" else perf_a_suffix
                
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p_morph.id, sequence_order=1))
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_a.id, sequence_order=2))
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=suffix.id, sequence_order=3))
        
        db.session.commit()
        print("Seeded A-stem morphemes.")

        # ==========================================
        # -yo'ten (Page 156) - Irregular
        # ==========================================
        verb_y = Verb.query.filter_by(root="-yo'ten").first()
        root_y = get_morph("-yo'ten-", "root", "work", None, "Root: Work")
        hab_y_suffix = get_morph("-s", "suffix", "habitual_marker_y", None, "Habitual Suffix")
        perf_y_suffix = get_morph(":on", "suffix", "perfective_marker_y", None, "Perfective Suffix")

        y_prefixes = {
            "habitual": {
                "1sg": "waky", "2sg": "say", "3m/i": "roy", "3f": "yakoy",
                "1du.ex": "yonkeniy", "1du.in": "yonkeniy", "2du": "seniy",
                "1pl.ex": "yonkway", "1pl.in": "yonkway", "2pl": "seway",
                "3pl.m": "ratiy", "3pl.f": "yotiy"
            },
            "perfective": {
                "1sg": "waky", "2sg": "say", "3m/i": "roy", "3f": "yakoy",
                "1du.ex": "yonkeniy", "1du.in": "yonkeniy", "2du": "seniy",
                "1pl.ex": "yonkway", "1pl.in": "yonkway", "2pl": "seway",
                "3pl.m": "ratiy", "3pl.f": "yotiy"
            }
        }

        for aspect, subjects in y_prefixes.items():
            for subject, prefix_text in subjects.items():
                vf = VocabForm.query.filter_by(verb_id=verb_y.id, form_type=aspect, subject=subject).first()
                if not vf: continue
                
                FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
                
                p_morph = get_morph(prefix_text, "prefix", f"{subject}_{aspect}_y", "Red", f"{subject} {aspect}")
                suffix = hab_y_suffix if aspect == "habitual" else perf_y_suffix
                
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p_morph.id, sequence_order=1))
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_y.id, sequence_order=2))
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=suffix.id, sequence_order=3))
        
        db.session.commit()
        print("Seeded -yo'ten morphemes.")

if __name__ == "__main__":
    seed_morphemes()
