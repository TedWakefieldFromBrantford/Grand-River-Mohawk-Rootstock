import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def seed_transitive():
    app = create_app()
    with app.app_context():
        def get_morph(text, m_type, func, color, label):
            m = Morpheme.query.filter_by(text=text, type=m_type, grammatical_function=func).first()
            if not m:
                m = Morpheme(text=text, type=m_type, grammatical_function=func, color_code=color, ui_label=label)
                db.session.add(m)
                db.session.commit()
            return m

        # The four verbs from Unit 2
        verbs_data = [
            {"root": "-nòn:we's", "gloss": "like", "root_text": "nòn:we's"},
            {"root": "-yenté:ri", "gloss": "know", "root_text": "yenté:ri"},
            {"root": "-norónhkwa", "gloss": "love", "root_text": "norónhkwa"},
            {"root": "-hswenhs", "gloss": "hate", "root_text": "hswenhs"},
        ]

        for vd in verbs_data:
            verb = Verb.query.filter_by(root=vd["root"]).first()
            if not verb:
                print(f"Verb {vd['root']} not found. Skipping.")
                continue

            # Create the root morpheme
            root_m = get_morph(vd["root_text"], "root", f"{vd['gloss']}_root", None, f"Root: {vd['gloss']}")
            
            # Page 40: "I -> it" prefix is "ke-"
            prefix_ke = get_morph("ke-", "prefix", "1sg_to_3m/i", "Red", "1st Person -> It")
            
            # Find the Habitual VocabForm for 1sg > 3m/i
            # Note: In the DB we imported earlier, the subject was "1sg". 
            # We need to update it to reflect the transitive nature.
            vf = VocabForm.query.filter_by(verb_id=verb.id, subject="1sg").first()
            
            if vf:
                vf.object = "3m/i"
                vf.english_gloss = f"I {vd['gloss']} it"
                FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
                
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=prefix_ke.id, sequence_order=1))
                db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_m.id, sequence_order=2))
                db.session.commit()
                print(f"Seeded 1sg > 3m/i for {vd['root']}")

if __name__ == "__main__":
    seed_transitive()
