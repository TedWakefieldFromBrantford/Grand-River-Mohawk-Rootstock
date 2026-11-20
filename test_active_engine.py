# test_active_engine.py
import pytest
from app import create_app
from models import db, Verb, VocabForm
from active_engine import ActiveEngine

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        yield app

def test_all_imported_verbs(app):
    with app.app_context():
        verbs = Verb.query.all()
        assert len(verbs) > 0, "No verbs found in the database!"
        
        verified_count = 0
        legacy_count = 0
        
        for verb in verbs:
            if not verb.tags:
                continue
                
            stem_class = verb.tags[0].name.split(":")[1]
            
            # Only test the stem classes we have engines for
            if stem_class not in ["C", "A", "I", "irregular"]:
                pytest.skip(f"Skipping {verb.root} - no engine for {stem_class}")
                
            engine = ActiveEngine(verb, stem_class=stem_class)
            test_forms = VocabForm.query.filter_by(verb_id=verb.id).all()
            
            for vf in test_forms:
                # Only test Habitual and Perfective for now
                if vf.form_type not in ["habitual", "perfective"]:
                    continue
                
                # If the form has no morpheme trace, it's legacy data.
                # We will verify it against the DB but flag it as "unverified build".
                if not vf.morpheme_trace:
                    legacy_count += 1
                    result = engine.generate(aspect=vf.form_type, subject=vf.subject)
                    # The fallback should still produce the right surface form
                    assert result["surface_form"] == vf.form, f"Fallback failed for {verb.root} {vf.form_type} {vf.subject}"
                else:
                    # If it has a trace, the engine MUST derive it correctly.
                    verified_count += 1
                    result = engine.generate(aspect=vf.form_type, subject=vf.subject)
                    assert result["surface_form"] == vf.form, f"Derivation failed for {verb.root} ({stem_class}) {vf.form_type} {vf.subject}. Expected {vf.form}, got {result['surface_form']}"
        
        print(f"\n✅ Verified (derived from morphemes): {verified_count}")
        print(f"⚠️  Legacy (surface fallback): {legacy_count}")
