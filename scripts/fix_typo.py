import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, VocabForm

def fix_typo():
    app = create_app()
    with app.app_context():
        # Find the bad form
        vf = VocabForm.query.filter_by(form="wesenkhón:ni'").first()
        if vf:
            vf.form = "wesenikhón:ni'"
            # Also fix the trace morpheme if it was hardcoded
            for trace in vf.morpheme_trace:
                if trace.morpheme.text == "wesen":
                    trace.morpheme.text = "wesen-i" # Or whatever makes sense for your UI
            db.session.commit()
            print("Fixed typo: wesenkhón:ni' -> wesenikhón:ni'")
        else:
            print("Could not find the form to fix. It might have a different typo.")

if __name__ == "__main__":
    fix_typo()
