import json
import sys
from flask import Flask
from models import db, Verb, VocabForm, Vocab

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

def import_batch(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with app.app_context():
        added_verbs = 0
        added_forms = 0
        updated_forms = 0

        for v_data in data.get("verbs", []):
            root = v_data['target_verb_root']
            gloss = v_data['target_verb_gloss']
            lesson_id = v_data.get("lesson_id") # Will be None if not in JSON
            
            verb = Verb.query.filter_by(root=root).first()
            if not verb:
                verb = Verb(lesson_id=lesson_id, root=root, gloss=gloss, forms_json={})
                db.session.add(verb)
                db.session.flush() 
                added_verbs += 1
            
            for f_data in v_data['forms']:
                # Option C: Find existing form by verb and the exact Mohawk text
                existing = VocabForm.query.filter_by(verb_id=verb.id, form=f_data['form']).first()
                
                if existing:
                    # Append the new gloss if it's not already there
                    new_gloss = f_data.get('english_gloss', '')
                    if new_gloss and new_gloss not in existing.english_gloss:
                        if existing.english_gloss:
                            existing.english_gloss += f" / {new_gloss}"
                        else:
                            existing.english_gloss = new_gloss
                    # Append notes if new
                    new_notes = f_data.get('notes', '')
                    if new_notes and new_notes not in existing.notes:
                        if existing.notes:
                            existing.notes += f", {new_notes}"
                        else:
                            existing.notes = new_notes
                    updated_forms += 1
                else:
                    new_form = VocabForm(
                        verb_id=verb.id,
                        form=f_data['form'],
                        form_type=f_data.get('form_type', 'citation'),
                        subject=f_data.get('subject', ''),
                        object=f_data.get('object', ''),
                        english_gloss=f_data.get('english_gloss', ''),
                        notes=f_data.get('notes', ''),           # <-- FIXED
                        source_batch=data.get('batch_id', ''),
                        source_page=data.get('source_pages', '')
                    )
                    db.session.add(new_form)
                    added_forms += 1
                
        db.session.commit()
        print(f"Import complete: {added_verbs} new verbs, {added_forms} new forms, {updated_forms} merged forms.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_batch.py batches/your-file.json")
        sys.exit(1)
    import_batch(sys.argv[1])
