# scripts/check_stats.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def check_stats():
    app = create_app()
    with app.app_context():
        verbs = Verb.query.all()
        print(f"Total verbs: {len(verbs)}")
        for v in verbs:
            form_count = VocabForm.query.filter_by(verb_id=v.id).count()
            trace_count = sum(len(vf.morpheme_trace) for vf in v.forms)
            print(f"  {v.root:15} | Forms: {form_count:3} | Traced: {trace_count:3}")
        
        print(f"\nTotal Morphemes in DB: {Morpheme.query.count()}")
        print(f"Total FormMorphemes: {FormMorpheme.query.count()}")

if __name__ == "__main__":
    check_stats()
