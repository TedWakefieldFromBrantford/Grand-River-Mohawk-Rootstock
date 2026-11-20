# check_sentinels.py
from app import create_app
from models import db, VocabForm, Verb
app = create_app()
with app.app_context():
    # Show every form with NULL or '' object, grouped by verb root
    bad = VocabForm.query.filter((VocabForm.object == None) | (VocabForm.object == "")).all()
    print(f"Total NULL/'' rows: {len(bad)}")
    from collections import Counter
    by_root = Counter((vf.verb.root if vf.verb else f"vocab:{vf.vocab.mohawk}"[:30]) for vf in bad)
    for root, n in by_root.most_common():
        print(f"  {n:3d}  {root}")
    print()
    # Sanity: show 5 sample forms that will be changed
    for vf in bad[:5]:
        print(f"  subject={vf.subject!r:12} object={vf.object!r:6} form={vf.form!r}")
