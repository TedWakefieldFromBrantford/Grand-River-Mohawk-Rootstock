from app import create_app
from models import db, VocabForm, Verb

app = create_app()
with app.app_context():
    print("DB URI:", db.engine.url)
    print("vocab_form count:", VocabForm.query.count())
    print("object=NULL count:", VocabForm.query.filter_by(object=None).count())
    print("object='' count:", VocabForm.query.filter_by(object="").count())
    print("object='3m/i' count:", VocabForm.query.filter_by(object="3m/i").count())
