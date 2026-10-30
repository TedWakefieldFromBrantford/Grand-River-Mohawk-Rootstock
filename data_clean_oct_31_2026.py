from app import app
from models import db, Vocab
with app.app_context():
    # Standardize category spelling
    for v in Vocab.query.filter(Vocab.category.in_(['color', 'colour'])).all():
        v.category = 'colour'
    # Fix capitalization on the dupes (keep lowercase, more likely correct for Mohawk citation)
    for v in Vocab.query.filter(Vocab.mohawk.in_(['Onekwénhtara', 'Kará:ken'])).all():
        # Delete the uppercase duplicates
        db.session.delete(v)
    db.session.commit()
    print("Cleaned.")
