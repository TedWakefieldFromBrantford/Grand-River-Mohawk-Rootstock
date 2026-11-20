import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Verb, VocabForm, Tag, VerbTag, Lesson

def import_a_stem():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.filter_by(week_number=5).first()
        
        verb = Verb.query.filter_by(root="-atketskw").first()
        if not verb:
            verb = Verb(lesson_id=lesson.id, root="-atketskw", gloss="get up", forms_json={})
            db.session.add(verb)
            db.session.commit()
            
            tag = Tag.query.filter_by(name="stem:A").first()
            if not tag:
                tag = Tag(name="stem:A")
                db.session.add(tag)
                db.session.commit()
            db.session.add(VerbTag(verb_id=verb.id, tag_id=tag.id))
            db.session.commit()

        data = [
            ("habitual", "1sg", "katkétskwas", "I get up"),
            ("habitual", "2sg", "satkétskwas", "you get up"),
            ("habitual", "3m/i", "ratkétskwas", "he/it gets up"),
            ("habitual", "3f", "yontkétskwas", "she gets up"),
            ("perfective", "1sg", "wakatkétskwen", "I have gotten up"),
            ("perfective", "2sg", "satkétskwen", "you have gotten up"),
            ("perfective", "3m/i", "rotkétskwen", "he/it has gotten up"),
            ("perfective", "3f", "yakotkétskwen", "she has gotten up"),
        ]

        for aspect, subject, form, gloss in data:
            exists = VocabForm.query.filter_by(verb_id=verb.id, form=form, form_type=aspect).first()
            if not exists:
                vf = VocabForm(
                    verb_id=verb.id, form=form, form_type=aspect, subject=subject,
                    english_gloss=gloss, attrs_json={"stem_class": "A"}, source_page="157"
                )
                db.session.add(vf)
        
        db.session.commit()
        print("Imported A-stem -atketskw forms.")

if __name__ == "__main__":
    import_a_stem()
