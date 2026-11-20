# quick split.py
from app import create_app
from models import db, VocabForm
from collections import Counter
app = create_app()
with app.app_context():
    for sentinel, label in [(None, "NULL"), ("", "empty")]:
        rows = VocabForm.query.filter_by(object=sentinel).all()
        roots = Counter(vf.verb.root if vf.verb else "vocab" for vf in rows)
        print(f"--- object {label} ({len(rows)} rows) ---")
        for r, n in roots.most_common(): print(f"  {n:3d}  {r}")
