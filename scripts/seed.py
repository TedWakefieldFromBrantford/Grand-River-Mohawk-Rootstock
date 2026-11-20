from app import app
from models import db, Lesson, Vocab, Verb

# STUB DATA — NOT Grand River. Source: eCampusOntario colors page.
# Replace entirely with official 2026-27 Ohsweken textbook content.
STUB = {
    "lesson": {"week_number": 4, "title": "STUB — colors + like (do not ship)",
               "notes": "placeholder only; replace with real lesson 4"},
    "vocab": [
        {"mohawk": "Onekwénhtara", "english": "red",   "category": "color", "prefix_color": "red"},
        {"mohawk": "Oròn:ia",      "english": "blue",  "category": "color", "prefix_color": "blue"},
        {"mohawk": "Kará:ken",     "english": "white", "category": "color", "prefix_color": "purple"},
    ],
    "verb": {"root": "STUB-root", "gloss": "like",
             "forms_json": {"1sg": "STUB-1sg", "2sg": "STUB-2sg",
                            "3m": "STUB-3m", "3f": "STUB-3f"}},
}

def seed():
    with app.app_context():
        db.drop_all(); db.create_all()
        l = Lesson(**STUB["lesson"]); db.session.add(l); db.session.flush()
        for v in STUB["vocab"]:
            db.session.add(Vocab(lesson_id=l.id, **v))
        db.session.add(Verb(lesson_id=l.id, **STUB["verb"]))
        db.session.commit()
        print(f"Seeded lesson {l.id} (week {l.week_number}) with stub data.")

if __name__ == "__main__":
    seed()
