# scripts/fix_a_stem_typo.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, VocabForm

def fix_typo():
    app = create_app()
    with app.app_context():
        # Find the bad form
        vf = VocabForm.query.filter_by(form="rotatkétskwen").first()
        if vf:
            vf.form = "rotkétskwen"
            db.session.commit()
            print("Fixed typo: rotatkétskwen -> rotkétskwen")
        else:
            print("Could not find the form to fix. Maybe the import script had a different typo?")

if __name__ == "__main__":
    fix_typo()
