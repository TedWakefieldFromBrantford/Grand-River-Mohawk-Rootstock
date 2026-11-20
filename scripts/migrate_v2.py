import models
import os
import json
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "mohawk.db")

# We make a backup just in case!
BACKUP_PATH = os.path.join(BASE_DIR, "instance", "mohawk_backup_before_v2.db")
if not os.path.exists(BACKUP_PATH):
    print(f"Making a backup at {BACKUP_PATH}...")
    import shutil
    shutil.copy2(DB_PATH, BACKUP_PATH)

# 2. Connect to the DB
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

print("Starting migration to Schema v2...")

# 3. Create the new tables
# We are importing db and our new models from models_v2.py
from models import db, Vocab, Verb
from models_v2 import db, VocabForm, Example, Tag, VocabTag
db.metadata.create_all(engine) 
print("-> Created new tables: vocab_form, example, tag, vocab_tag.")

# 4. Move the old 'forms_json' data into 'vocab_form'
# First, let's find all the verbs that currently have forms_json data.
# We query the old table structure directly.
old_verbs = session.execute(text("SELECT id, root, forms_json FROM verb WHERE forms_json IS NOT NULL")).fetchall()

for v_id, v_root, forms_json_str in old_verbs:
    try:
        # The DB stores it as a JSON string, we need to turn it back into a Python dictionary
        forms_dict = json.loads(forms_json_str) if isinstance(forms_json_str, str) else forms_json_str
        
        if not forms_dict:
            continue
            
        print(f"-> Migrating forms for verb: {v_root}")
        
        for person_key, mohawk_form in forms_dict.items():
            if not mohawk_form:
                continue
                
            # Create a new row in vocab_form for each person
            new_form = VocabForm(
                verb_id=v_id,
                form=mohawk_form,
                form_type="transitive",
                subject=person_key, # e.g., "1sg"
                object="3n",        # Assuming these are "it" forms based on your notes
                notes="Migrated from legacy forms_json",
                source_batch="legacy"
            )
            session.add(new_form)
            
        # Optional: We could clear the old forms_json here so we don't do this twice.
        # But we'll leave it for now as a safety net.
        
    except Exception as e:
        print(f"Error migrating {v_root}: {e}")

# 5. Save changes
session.commit()
print("Migration complete! Your data is safe.")
