# test_transitive_engine.py
import pytest
from app import create_app
from models import db, Verb, VocabForm
from transitive_engine import TransitiveEngine

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        yield app

def test_transitive_verbs(app):
    with app.app_context():
        verbs = Verb.query.filter(Verb.root.in_(["-nòn:we's", "-yenté:ri", "-norónhkwa", "-hswenhs"])).all()
        assert len(verbs) == 4, "Did not find all 4 transitive verbs."
        
        for verb in verbs:
            engine = TransitiveEngine(verb)
            forms = VocabForm.query.filter_by(verb_id=verb.id).all()
            
            for vf in forms:
                if not vf.morpheme_trace:
                    pytest.skip(f"Skipping {vf.form} - no trace")
                    
                # KEY FIX: Use vf.object (which may be None) instead of hardcoding "3m/i"
                result = engine.generate(aspect=vf.form_type, subject=vf.subject, obj=vf.object)
                assert result["surface_form"] == vf.form, f"Failed for {vf.form} ({vf.subject} > {vf.object}). Expected {vf.form}, got {result['surface_form']}"
