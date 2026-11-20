# check_counts.py
from app import create_app
from models import db, Verb, VocabForm

app = create_app()
with app.app_context():
    verbs = Verb.query.all()
    for v in verbs:
        count = VocabForm.query.filter_by(verb_id=v.id).count()
        if count > 0:
            print(f"{v.root}: {count} forms")
