# scripts/fix_hse.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, VocabForm, Morpheme, FormMorpheme

def fix():
    app = create_app()
    with app.app_context():
        vf = VocabForm.query.filter_by(form="hsènòn:we's").first()
        if not vf:
            print("Form not found!")
            return
        
        # Normalize the aspect
        vf.form_type = "habitual"
        
        # Find or create the hse- prefix morpheme
        p = Morpheme.query.filter_by(text="hse", type="prefix", grammatical_function="2sg_to_3m/i").first()
        if not p:
            p = Morpheme(text="hse", type="prefix", grammatical_function="2sg_to_3m/i", color_code="Red", ui_label="2sg -> 3m/i")
            db.session.add(p)
            db.session.commit()
        
        # Clear old trace and add the correct one
        FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
        db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p.id, sequence_order=1))
        
        # Add the root (it already exists in the DB from the backfill)
        root = Morpheme.query.filter_by(text="nòn:we's", type="root").first()
        db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root.id, sequence_order=2))
        
        db.session.commit()
        print(f"Fixed: {vf.form} (subject={vf.subject}, object={vf.object}, form_type={vf.form_type})")
        print(f"Trace now has {len(vf.morpheme_trace)} morphemes.")

if __name__ == "__main__":
    fix()
