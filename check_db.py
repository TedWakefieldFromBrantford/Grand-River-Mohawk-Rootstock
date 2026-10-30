from app import app
from models import db, Verb, Vocab, VocabForm

with app.app_context():
    print("--- DB CHECK ---\n")
    
    print(f"VOCAB ({Vocab.query.count()} total):")
    for v in Vocab.query.all():
        print(f"  [{v.category or '-'}] {v.mohawk} = {v.english}  (lesson: {v.lesson_id})")
    
    print(f"\nVERBS ({Verb.query.count()} total):")
    for v in Verb.query.all():
        print(f"  {v.root} = {v.gloss}  ({len(v.forms)} forms, lesson: {v.lesson_id})")
    
    print(f"\nFORMS: {VocabForm.query.count()} total\n")
    
    # Show a sample of forms per type
    print("Sample forms by type:")
    for ftype in ["transitive", "reflexive", "reciprocal"]:
        forms = VocabForm.query.filter_by(form_type=ftype).limit(3).all()
        print(f"  {ftype}:")
        for f in forms:
            print(f"    {f.form} ({f.subject}->{f.object}) = '{f.english_gloss}' [{f.notes}]")
