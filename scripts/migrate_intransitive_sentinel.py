# migrate_intransitive_sentinel.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, VocabForm
app = create_app()
with app.app_context():
    rows = VocabForm.query.filter((VocabForm.object == None) | (VocabForm.object == "")).all()
    print(f"Updating {len(rows)} rows: object NULL/'' -> '3m/i'")
    for vf in rows:
        vf.object = "3m/i"
    db.session.commit()
    print("Done. Verifying...")
    print("remaining NULL:", VocabForm.query.filter_by(object=None).count())
    print("remaining '':", VocabForm.query.filter_by(object="").count())
    print("now '3m/i':", VocabForm.query.filter_by(object="3m/i").count())
