# scripts/debug_wake.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, VocabForm

def debug():
    app = create_app()
    with app.app_context():
        vf = VocabForm.query.filter_by(form="wakenòn:we's").first()
        if not vf:
            print("Form not found!")
            return
        print(f"Form: {vf.form}")
        print(f"Subject: {vf.subject}")
        print(f"Object: {vf.object}")
        print(f"Trace count: {len(vf.morpheme_trace)}")
        for t in vf.morpheme_trace:
            print(f"  {t.sequence_order}: {t.morpheme.text} ({t.morpheme.type})")

if __name__ == "__main__":
    debug()
