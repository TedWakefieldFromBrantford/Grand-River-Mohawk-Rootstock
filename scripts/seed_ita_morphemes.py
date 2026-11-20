import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm, Morpheme, FormMorpheme

def seed_ita():
    app = create_app()
    with app.app_context():
        verb = Verb.query.filter_by(root="-ita").first()
        if not verb: return

        # Clean up old I-stem morphemes
        Morpheme.query.filter(Morpheme.grammatical_function.like("%_I")).delete()
        db.session.commit()

        def get_morph(text, m_type, func, color, label):
            m = Morpheme.query.filter_by(text=text, type=m_type, grammatical_function=func).first()
            if not m:
                m = Morpheme(text=text, type=m_type, grammatical_function=func, color_code=color, ui_label=label)
                db.session.add(m)
                db.session.commit()
            return m

        # Define exact chunks for Habitual and Perfective
        hab_prefixes = {
            "1sg": "wakí:", "2sg": "sén:", "3m/i": "ró:", "3f": "yakó:",
            "1du.ex": "yonkén:", "1du.in": "yonkén:", "2du": "sení:",
            "1pl.ex": "yonkwén:", "1pl.in": "yonkwén:", "2pl": "sewén:",
            "3pl.m": "róti:", "3pl.f": "yóti:"
        }
        perf_prefixes = {
            "1sg": "waki", "2sg": "sen", "3m/i": "ro", "3f": "yako",
            "1du.ex": "yonken", "1du.in": "yonken", "2du": "seni",
            "1pl.ex": "yonkwen", "1pl.in": "yonkwen", "2pl": "sewen",
            "3pl.m": "roti", "3pl.f": "yoti"
        }

        root_hab = get_morph("tah", "root", "sleep_hab_root", None, "Root (Hab): tah")
        root_perf = get_morph("tá:'on", "root", "sleep_perf_root", None, "Root (Perf): tá:'on")
        hab_suffix = get_morph("s", "suffix", "habitual_marker_I", None, "Habitual Suffix (I-stem)")

        for subject, prefix_text in hab_prefixes.items():
            vf = VocabForm.query.filter_by(verb_id=verb.id, form_type="habitual", subject=subject).first()
            if not vf: continue
            FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
            
            p = get_morph(prefix_text, "prefix", f"{subject}_habitual_I", "Red", f"{subject} Habitual")
            db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p.id, sequence_order=1))
            db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_hab.id, sequence_order=2))
            db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=hab_suffix.id, sequence_order=3))

        for subject, prefix_text in perf_prefixes.items():
            vf = VocabForm.query.filter_by(verb_id=verb.id, form_type="perfective", subject=subject).first()
            if not vf: continue
            FormMorpheme.query.filter_by(vocab_form_id=vf.id).delete()
            
            p = get_morph(prefix_text, "prefix", f"{subject}_perfective_I", "Purple", f"{subject} Perfective")
            db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=p.id, sequence_order=1))
            db.session.add(FormMorpheme(vocab_form_id=vf.id, morpheme_id=root_perf.id, sequence_order=2))

        db.session.commit()
        print("Re-seeded -ita with exact phonological chunks.")

if __name__ == "__main__":
    seed_ita()
