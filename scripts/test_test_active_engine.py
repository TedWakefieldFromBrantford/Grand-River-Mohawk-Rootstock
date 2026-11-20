import pytest
from app import create_app
from models import db, Verb, VocabForm
from active_engine import ActiveEngine

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:" 
    })
    with app.app_context():
        db.create_all()
        yield app

def test_all_imported_verbs(app):
    with app.app_context():
        # Get all verbs that have forms in the DB
        verbs = Verb.query.all()
        
        for verb in verbs:
            if not verb.tags:
                continue
                
            stem_class = verb.tags[0].name.split(":")[1]
            
            # Skip stem classes we haven't built the engine for yet
            if stem_class not in ["C"]:
                pytest.skip(f"Skipping {verb.root} - Engine does not support stem class {stem_class} yet")
                
            engine = ActiveEngine(verb, stem_class=stem_class)
            test_forms = VocabForm.query.filter_by(verb_id=verb.id).all()
            
            for vf in test_forms:
                # Skip forms we haven't built rules for yet (only doing habitual/perfective for now)
                if vf.form_type not in ["habitual", "perfective"]:
                    continue
                    
                result = engine.generate(aspect=vf.form_type, subject=vf.subject)
                assert result["surface_form"] == vf.form, f"Failed for {verb.root} ({stem_class}) {vf.form_type} {vf.subject}. Expected {vf.form}, got {result['surface_form']}"
