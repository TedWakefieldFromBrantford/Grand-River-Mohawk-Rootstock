# scripts/fix_hse_typo.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, VocabForm

def fix_typo():
    app = create_app()
    with app.app_context():
        # Find the wrongly-accented form from Week 1
        vf = VocabForm.query.filter_by(form="hsènòn:we's").first()
        if vf:
            vf.form = "hsenòn:we's"  # Remove the accent on the 'e'
            db.session.commit()
            print("Fixed: hsènòn:we's -> hsenòn:we's")
        else:
            print("Form not found. Checking for the correct form...")
            vf2 = VocabForm.query.filter_by(form="hsenòn:we's").first()
            if vf2:
                print("The database already has the correct form: hsenòn:we's")

if __name__ == "__main__":
    fix_typo()
