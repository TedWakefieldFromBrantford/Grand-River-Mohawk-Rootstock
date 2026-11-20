# scripts/debug_hse.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, VocabForm

def debug():
    app = create_app()
    with app.app_context():
        vf = VocabForm.query.filter_by(form="hsènòn:we's").first()
        if not vf:
            print("Form not found in DB!")
            return
        
        print(f"Form: {vf.form}")
        print(f"Subject: {vf.subject}")
        print(f"Object: {vf.object}")
        print(f"Aspect: {vf.form_type}")
        print(f"Trace count: {len(vf.morpheme_trace)}")
        
        if vf.morpheme_trace:
            for t in vf.morpheme_trace:
                print(f"  {t.sequence_order}: {t.morpheme.text} ({t.morpheme.type})")
        else:
            print("  NO MORPHEME TRACE!")

if __name__ == "__main__":
    debug()
