# scripts/fix_ita_3f.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Morpheme, VocabForm, FormMorpheme

def fix_ita_3f():
    app = create_app()
    with app.app_context():
        # Find the bad morpheme
        bad = Morpheme.query.filter_by(text="yó:", type="prefix", grammatical_function="3f_habitual_I").first()
        if bad:
            bad.text = "yakó:"
            db.session.commit()
            print("Fixed 3f Habitual prefix: yó: -> yakó:")
        else:
            print("Could not find the bad morpheme.")
            
        # Also check the 3m/i to be safe
        bad_3m = Morpheme.query.filter_by(text="ró:", type="prefix", grammatical_function="3m_habitual_I").first()
        if bad_3m:
            print(f"3m/i prefix is: {bad_3m.text} (should be ró:)")

if __name__ == "__main__":
    fix_ita_3f()
