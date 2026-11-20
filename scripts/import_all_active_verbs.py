import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Verb, VocabForm, Tag, VerbTag, Lesson

def import_all():
    app = create_app()
    with app.app_context():
        lesson = Lesson.query.filter_by(week_number=5).first()
        if not lesson:
            lesson = Lesson(week_number=5, title="Unit 5: Active Verbs")
            db.session.add(lesson)
            db.session.commit()

        def get_or_create_verb(root, gloss, stem_class, notes=""):
            verb = Verb.query.filter_by(root=root).first()
            if not verb:
                verb = Verb(lesson_id=lesson.id, root=root, gloss=gloss, forms_json={}, notes=notes)
                db.session.add(verb)
                db.session.commit()
                
                tag = Tag.query.filter_by(name=f"stem:{stem_class}").first()
                if not tag:
                    tag = Tag(name=f"stem:{stem_class}")
                    db.session.add(tag)
                    db.session.commit()
                db.session.add(VerbTag(verb_id=verb.id, tag_id=tag.id))
                db.session.commit()
            return verb

        def add_forms(verb, data_list):
            count = 0
            for aspect, subject, form, gloss in data_list:
                exists = VocabForm.query.filter_by(verb_id=verb.id, form=form, form_type=aspect).first()
                if not exists:
                    vf = VocabForm(
                        verb_id=verb.id,
                        form=form,
                        form_type=aspect,
                        subject=subject,
                        english_gloss=gloss,
                        attrs_json={"aspect_standard": aspect, "stem_class": verb.tags[0].name.split(":")[1] if verb.tags else "unknown"},
                        source_page="Active Unit 5"
                    )
                    db.session.add(vf)
                    count += 1
            db.session.commit()
            print(f"Added {count} forms for {verb.root}")

        # ==========================================
        # 1. C-Stem: -yo'ten (work) - Page 156
        # ==========================================
        verb_work = get_or_create_verb("-yo'ten", "work", "C")
        work_data = [
            ("habitual", "1sg", "wakyó'tens", "I work"), ("habitual", "2sg", "sayó'tens", "you work"),
            ("habitual", "3m/i", "róy'tens", "he/it works"), ("habitual", "3f", "yakoyó'tens", "she works"),
            ("habitual", "1du.ex", "yonkeniyó'tens", "you & I work"), ("habitual", "1du.in", "yonkeniyó'tens", "s.o. & I work"),
            ("habitual", "2du", "seniyó'tens", "you two work"), ("habitual", "1pl.ex", "yonkwayó'tens", "you all & I work"),
            ("habitual", "1pl.in", "yonkwayó'tens", "they & I work"), ("habitual", "2pl", "sewayó'tens", "you all work"),
            ("habitual", "3pl.m", "ratiyó'tens", "they Ms work"), ("habitual", "3pl.f", "yotiyó'tens", "they Fs work"),
            # ... (You would paste the rest of the perfective/definite/etc. forms here. 
            # I'm just doing a subset for now to keep the script manageable, but you can add all 60)
        ]
        add_forms(verb_work, work_data)

        # ==========================================
        # 2. A-Stem: -atketskw (get up) - Page 157
        # ==========================================
        verb_getup = get_or_create_verb("-atketskw", "get up", "A")
        getup_data = [
            ("habitual", "1sg", "katkétskwas", "I get up"), 
            ("habitual", "2sg", "satkétskwas", "you get up"),
            ("habitual", "3m/i", "ratkétskwas", "he/it gets up"), 
            ("habitual", "3f", "yontkétskwas", "she gets up"),
            ("perfective", "1sg", "wakatkétskwen", "I have gotten up"),
            ("perfective", "2sg", "satkétskwen", "you have gotten up"),
            ("definite", "1sg", "wa'katkétsko'", "I got up (1x)"),
            ("definite", "2sg", "wahsatkétsko'", "you got up (1x)"),
        ]
        add_forms(verb_getup, getup_data)

        # ==========================================
        # 3. I-Stem: -ita (sleep) - Page 164
        # ==========================================
        verb_sleep = get_or_create_verb("-ita", "sleep", "I")
        sleep_data = [
            ("habitual", "1sg", "wakí:tahs", "I sleep"), 
            ("habitual", "2sg", "sén:tahs", "you sleep"),
            ("habitual", "3m/i", "ró:tahs", "he/it sleeps"), 
            ("habitual", "3f", "yakó:tahs", "she sleeps"),
            ("perfective", "1sg", "wakitá:'on", "I have slept"),
            ("definite", "1sg", "onkí:tahwe'", "I slept (1x)"),
        ]
        add_forms(verb_sleep, sleep_data)

        # ==========================================
        # 4. Irregular: -i:ron (say) - Page 163
        # ==========================================
        verb_say = get_or_create_verb("-i:ron", "say", "irregular")
        say_data = [
            ("habitual", "1sg", "ká:ton", "I say"), 
            ("habitual", "2sg", "sá:ton", "you say"),
            ("habitual", "3m/i", "rá:ton", "he/it says"), 
            ("habitual", "3f", "yón:ton", "she says"),
            ("perfective", "1sg", "wá:ken", "I have said"),
            ("definite", "1sg", "wa'kí:ron'", "I said (1x)"),
        ]
        add_forms(verb_say, say_data)

if __name__ == "__main__":
    import_all()
