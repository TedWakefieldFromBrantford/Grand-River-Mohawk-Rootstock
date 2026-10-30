"""
One-off cleanup: remove the hallucinated 'hate' verb and its forms,
then re-import the corrected batch. Run with --dry-run first.
"""
import argparse, sys, json
from flask import Flask
from models import db, Verb, VocabForm

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

BAD_ROOTS = ["-kons", "kons", "-kóns"]  # whatever hallucinated form you have
GOOD_ROOT = "-hswenhs"
BATCH_FILE = "batches/unit2_hate_corrected.json"

def dry_run(bad_verbs):
    for v in bad_verbs:
        n = VocabForm.query.filter_by(verb_id=v.id).count()
        print(f"  would delete Verb(id={v.id}, root={v.root!r}) and {n} forms")
    print(f"  would import {BATCH_FILE}")

def do_delete(bad_verbs):
    for v in bad_verbs:
        VocabForm.query.filter_by(verb_id=v.id).delete(synchronize_session=False)
        db.session.delete(v)
        print(f"  deleted Verb(id={v.id}, root={v.root!r})")
    db.session.commit()

def do_import(path):
    from import_batch import import_batch
    import_batch(path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reimport", action="store_true")
    args = ap.parse_args()

    with app.app_context():
        bad = Verb.query.filter(Verb.root.in_(BAD_ROOTS)).all()
        # Also catch anything whose gloss is 'hate' but root is wrong
        bad += [v for v in Verb.query.filter_by(gloss="hate").all() if v.root != GOOD_ROOT]
        # De-dupe
        bad = list({v.id: v for v in bad}.values())

        if not bad:
            print("No bad 'hate' verb found. Already clean?")
        elif args.dry_run or not (args.apply or args.reimport):
            dry_run(bad)
        elif args.apply:
            do_delete(bad)

        if args.reimport:
            do_import(BATCH_FILE)
