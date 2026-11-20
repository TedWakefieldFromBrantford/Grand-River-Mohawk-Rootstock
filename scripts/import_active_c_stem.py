import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Verb, VocabForm, Tag, VerbTag, Lesson, Morpheme, FormMorpheme

def import_c_stem_cook():
    # 1. Create the app
    app = create_app()
    
    # 2. Push the app context so the DB works
    with app.app_context():
        # --- Ensure Lesson exists ---
        lesson = Lesson.query.filter_by(week_number=5).first()
        if not lesson:
            lesson = Lesson(week_number=5, title="Unit 5: Active Verbs")
            db.session.add(lesson)
            db.session.commit()

        # --- Create/Find the Verb ---
        verb = Verb.query.filter_by(root="-khonn-").first()
        if not verb:
            verb = Verb(
                lesson_id=lesson.id,
                root="-khonn-",
                gloss="cook",
                forms_json={}, 
                notes="Typical C-Stem verb. See chart on Page 155."
            )
            db.session.add(verb)
            db.session.commit()

        # --- Tag the Stem Class ---
        c_stem_tag = Tag.query.filter_by(name="stem:C").first()
        if not c_stem_tag:
            c_stem_tag = Tag(name="stem:C")
            db.session.add(c_stem_tag)
            db.session.commit()
        if c_stem_tag not in verb.tags:
            db.session.add(VerbTag(verb_id=verb.id, tag_id=c_stem_tag.id))
            db.session.commit()

        # --- Helper to get/create Morphemes ---
        def get_morph(text, m_type, func, color, label, notes=""):
            m = Morpheme.query.filter_by(text=text, type=m_type).first()
            if not m:
                m = Morpheme(text=text, type=m_type, grammatical_function=func, 
                             color_code=color, ui_label=label, notes=notes)
                db.session.add(m)
                db.session.commit()
            return m

        # Define static morphemes for -khonn-
        root_m = get_morph("-khonn-", "root", "cook", None, "Root: Cook")
        
        # Suffixes
        hab_suffix = get_morph("-is", "suffix", "habitual_marker", None, "Habitual Suffix")
        perf_suffix = get_morph("-ni", "suffix", "perfective_marker", None, "Perfective Suffix")
        def_suffix = get_morph("-i'", "suffix", "definite_marker", None, "Definite/Past Suffix")
        indef_suffix = get_morph("-i'", "suffix", "indefinite_marker", None, "Indefinite/Conditional Suffix")
        fut_suffix = get_morph("-i'", "suffix", "future_marker", None, "Future Suffix")
        cmd_suffix = get_morph("-ni", "suffix", "command_marker", None, "Command Suffix")

        # --- Data Array (Same as before) ---
        data = [
            # HABITUAL
            ("habitual", "1sg", "kekhón:nis", "I do it", [(get_morph("k-", "prefix", "1sg_habitual", "Red", "1st Person Singular"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "2sg", "hsekhón:nis", "you do it", [(get_morph("hse-", "prefix", "2sg_habitual", "Red", "2nd Person Singular"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "3m/i", "rakhón:nis", "he/it does it", [(get_morph("ra-", "prefix", "3m_habitual", "Blue", "3rd Person Masc/Neut"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "3f", "yekhón:nis", "she does it", [(get_morph("ye-", "prefix", "3f_habitual", "Blue", "3rd Person Feminine"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "1du.ex", "tenikhón:nis", "you & I do it", [(get_morph("teni-", "prefix", "1du_ex_habitual", "Red", "1st Person Dual Exclusive"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "1du.in", "yakenikhón:nis", "s.o. & I do it", [(get_morph("yakeni-", "prefix", "1du_in_habitual", "Red", "1st Person Dual Inclusive"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "2du", "senikhón:nis", "you two do it", [(get_morph("seni-", "prefix", "2du_habitual", "Red", "2nd Person Dual"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "1pl.ex", "tewakhón:nis", "you all & I do it", [(get_morph("tewa-", "prefix", "1pl_ex_habitual", "Red", "1st Person Plural Exclusive"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "1pl.in", "yakwakhón:nis", "they & I do it", [(get_morph("yakwa-", "prefix", "1pl_in_habitual", "Red", "1st Person Plural Inclusive"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "2pl", "sewakhón:nis", "you all do it", [(get_morph("sewa-", "prefix", "2pl_habitual", "Red", "2nd Person Plural"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "3pl.m", "ratikhón:nis", "they Ms do it", [(get_morph("rati-", "prefix", "3pl_m_habitual", "Blue", "3rd Person Plural Masculine"), 1), (root_m, 2), (hab_suffix, 3)]),
            ("habitual", "3pl.f", "kontikhón:nis", "they Fs do it", [(get_morph("konti-", "prefix", "3pl_f_habitual", "Blue", "3rd Person Plural Feminine"), 1), (root_m, 2), (hab_suffix, 3)]),

            # PERFECTIVE
            ("perfective", "1sg", "wakekhón:ni", "I've done it", [(get_morph("wake-", "prefix", "1sg_perfective", "Purple", "1st Person Singular (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "2sg", "sakhón:ni", "you've done it", [(get_morph("sa-", "prefix", "2sg_perfective", "Purple", "2nd Person Singular (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "3m/i", "rokhón:ni", "he/it has done it", [(get_morph("ro-", "prefix", "3m_perfective", "Purple", "3rd Person Masc/Neut (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "3f", "yakokhón:ni", "she has done it", [(get_morph("yako-", "prefix", "3f_perfective", "Purple", "3rd Person Feminine (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "1du.ex", "yonkenikhón:ni", "you & I have done it", [(get_morph("yonkeni-", "prefix", "1du_ex_perfective", "Purple", "1st Person Dual Exclusive (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "1du.in", "yonkenikhón:ni", "s.o. & I have done it", [(get_morph("yonkeni-", "prefix", "1du_in_perfective", "Purple", "1st Person Dual Inclusive (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "2du", "senikhón:ni", "you two have done it", [(get_morph("seni-", "prefix", "2du_perfective", "Purple", "2nd Person Dual (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "1pl.ex", "yonkwakhón:ni", "you all & I have done it", [(get_morph("yonkwa-", "prefix", "1pl_ex_perfective", "Purple", "1st Person Plural Exclusive (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "1pl.in", "yonkwakhón:ni", "they & I have done it", [(get_morph("yonkwa-", "prefix", "1pl_in_perfective", "Purple", "1st Person Plural Inclusive (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "2pl", "sewakhón:ni", "you all have done it", [(get_morph("sewa-", "prefix", "2pl_perfective", "Purple", "2nd Person Plural (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "3pl.m", "rotikhón:ni", "they Ms have done it", [(get_morph("roti-", "prefix", "3pl_m_perfective", "Purple", "3rd Person Plural Masculine (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),
            ("perfective", "3pl.f", "yotikhón:ni", "they Fs have done it", [(get_morph("yoti-", "prefix", "3pl_f_perfective", "Purple", "3rd Person Plural Feminine (Perfective)"), 1), (root_m, 2), (perf_suffix, 3)]),

            # DEFINITE
            ("definite", "1sg", "wa'kékhon:ni'", "I did it (1x)", [(get_morph("wa'ké-", "prefix", "1sg_definite", "Purple", "1st Person Singular (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "2sg", "wahsekhón:ni'", "you did it (1x)", [(get_morph("wahse-", "prefix", "2sg_definite", "Purple", "2nd Person Singular (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "3m/i", "wahakhón:ni'", "he/it did it (1x)", [(get_morph("waha-", "prefix", "3m_definite", "Purple", "3rd Person Masc/Neut (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "3f", "wa'ékhon:ni'", "she did it (1x)", [(get_morph("wa'é-", "prefix", "3f_definite", "Purple", "3rd Person Feminine (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "1du.ex", "wetenikhón:ni'", "you & I did it (1x)", [(get_morph("weteni-", "prefix", "1du_ex_definite", "Purple", "1st Person Dual Exclusive (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "1du.in", "wa'akenikhón:ni'", "s.o. & I did it (1x)", [(get_morph("wa'akeni-", "prefix", "1du_in_definite", "Purple", "1st Person Dual Inclusive (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "2du", "wesenikhón:ni'", "you two did it (1x)", [(get_morph("wesen-", "prefix", "2du_definite", "Purple", "2nd Person Dual (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "1pl.ex", "wetewakhón:ni'", "you all & I did it (1x)", [(get_morph("wetewa-", "prefix", "1pl_ex_definite", "Purple", "1st Person Plural Exclusive (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "1pl.in", "wa'akwakhón:ni'", "they & I did it (1x)", [(get_morph("wa'akwa-", "prefix", "1pl_in_definite", "Purple", "1st Person Plural Inclusive (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "2pl", "wesewakhón:ni'", "you all did it (1x)", [(get_morph("wese-", "prefix", "2pl_definite", "Purple", "2nd Person Plural (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "3pl.m", "wahatikhón:ni'", "they Ms did it (1x)", [(get_morph("wahati-", "prefix", "3pl_m_definite", "Purple", "3rd Person Plural Masculine (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),
            ("definite", "3pl.f", "wa'kontikhón:ni'", "they Fs did it (1x)", [(get_morph("wa'konti-", "prefix", "3pl_f_definite", "Purple", "3rd Person Plural Feminine (Definite)"), 1), (root_m, 2), (def_suffix, 3)]),

            # INDEFINITE
            ("indefinite", "1sg", "akekhón:ni'", "I would do it", [(get_morph("ake-", "prefix", "1sg_indefinite", "Purple", "1st Person Singular (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "2sg", "ahsekhón:ni'", "you would do it", [(get_morph("ahse-", "prefix", "2sg_indefinite", "Purple", "2nd Person Singular (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "3m/i", "ahakhón:ni'", "he/it would do it", [(get_morph("aha-", "prefix", "3m_indefinite", "Purple", "3rd Person Masc/Neut (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "3f", "ayekhón:ni'", "she would do it", [(get_morph("aye-", "prefix", "3f_indefinite", "Purple", "3rd Person Feminine (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "1du.ex", "aetenikhón:ni'", "you & I would do it", [(get_morph("aeteni-", "prefix", "1du_ex_indefinite", "Purple", "1st Person Dual Exclusive (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "1du.in", "ayakenikhón:ni'", "s.o. & I would do it", [(get_morph("ayakeni-", "prefix", "1du_in_indefinite", "Purple", "1st Person Dual Inclusive (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "2du", "aesenikhón:ni'", "you two would do it", [(get_morph("aeseni-", "prefix", "2du_indefinite", "Purple", "2nd Person Dual (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "1pl.ex", "aetewakhón:ni'", "you all & I would do it", [(get_morph("aetewa-", "prefix", "1pl_ex_indefinite", "Purple", "1st Person Plural Exclusive (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "1pl.in", "ayakwakhón:ni'", "they & I would do it", [(get_morph("ayakwa-", "prefix", "1pl_in_indefinite", "Purple", "1st Person Plural Inclusive (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "2pl", "aesewakhón:ni'", "you all would do it", [(get_morph("aesewa-", "prefix", "2pl_indefinite", "Purple", "2nd Person Plural (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "3pl.m", "ahatikhón:ni'", "they Ms would do it", [(get_morph("ahati-", "prefix", "3pl_m_indefinite", "Purple", "3rd Person Plural Masculine (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),
            ("indefinite", "3pl.f", "akontikhón:ni'", "they Fs would do it", [(get_morph("akonti-", "prefix", "3pl_f_indefinite", "Purple", "3rd Person Plural Feminine (Indefinite)"), 1), (root_m, 2), (indef_suffix, 3)]),

            # FUTURE
            ("future", "1sg", "enkekhón:ni'", "I will do it", [(get_morph("enke-", "prefix", "1sg_future", "Purple", "1st Person Singular (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "2sg", "enhsekhón:ni'", "you will do it", [(get_morph("enhse-", "prefix", "2sg_future", "Purple", "2nd Person Singular (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "3m/i", "enhakhón:ni'", "he/it will do it", [(get_morph("enha-", "prefix", "3m_future", "Purple", "3rd Person Masc/Neut (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "3f", "enyekhón:ni'", "she will do it", [(get_morph("enye-", "prefix", "3f_future", "Purple", "3rd Person Feminine (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "1du.ex", "entenikhón:ni'", "you & I will do it", [(get_morph("enteni-", "prefix", "1du_ex_future", "Purple", "1st Person Dual Exclusive (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "1du.in", "enyakenikhón:ni'", "s.o. & I will do it", [(get_morph("enyakeni-", "prefix", "1du_in_future", "Purple", "1st Person Dual Inclusive (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "2du", "ensenikhón:ni'", "you two will do it", [(get_morph("enseni-", "prefix", "2du_future", "Purple", "2nd Person Dual (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "1pl.ex", "entewakhón:ni'", "you all & I will do it", [(get_morph("entewa-", "prefix", "1pl_ex_future", "Purple", "1st Person Plural Exclusive (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "1pl.in", "enyakwakhón:ni'", "they & I will do it", [(get_morph("enyakwa-", "prefix", "1pl_in_future", "Purple", "1st Person Plural Inclusive (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "2pl", "ensewakhón:ni'", "you all will do it", [(get_morph("ensewa-", "prefix", "2pl_future", "Purple", "2nd Person Plural (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "3pl.m", "enhatikhón:ni'", "they Ms will do it", [(get_morph("enhati-", "prefix", "3pl_m_future", "Purple", "3rd Person Plural Masculine (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
            ("future", "3pl.f", "enkontikhón:ni'", "they Fs will do it", [(get_morph("enkonti-", "prefix", "3pl_f_future", "Purple", "3rd Person Plural Feminine (Future)"), 1), (root_m, 2), (fut_suffix, 3)]),
        ]

        # --- Insert into DB ---
        for aspect, subject, form, gloss, trace in data:
            exists = VocabForm.query.filter_by(verb_id=verb.id, form=form, form_type=aspect).first()
            if not exists:
                vf = VocabForm(
                    verb_id=verb.id,
                    form=form,
                    form_type=aspect,
                    subject=subject,
                    english_gloss=gloss,
                    attrs_json={
                        "aspect_standard": aspect,
                        "aspect_textbook": aspect, 
                        "stem_class": "C",
                        "transitive": False
                    },
                    source_batch="Active Verbs Batch 1",
                    source_page="155"
                )
                db.session.add(vf)
                db.session.flush() # Get vf.id

                for morph, order in trace:
                    fm = FormMorpheme(
                        vocab_form_id=vf.id,
                        morpheme_id=morph.id,
                        sequence_order=order
                    )
                    db.session.add(fm)
        
        db.session.commit()
        print(f"Successfully imported forms and traces for {verb.root}")

if __name__ == "__main__":
    import_c_stem_cook()
