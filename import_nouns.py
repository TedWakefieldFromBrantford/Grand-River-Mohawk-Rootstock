import json
import sys
from flask import Flask
from models import db, Vocab

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

def import_nouns(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with app.app_context():
        added = 0
        for v_item in data.get("vocab", []):
            m = v_item.get("mohawk", "").strip()
            if not m:
                continue
            
            # Skip if already exists
            if Vocab.query.filter_by(mohawk=m).first():
                continue
                
            db.session.add(Vocab(
                mohawk=m,
                english=v_item.get("english", ""),
                category=v_item.get("category", ""),
                class_or_stem=v_item.get("class_or_stem", ""),
                notes=v_item.get("notes", "")
            ))
            added += 1
        
        db.session.commit()
        print(f"Import complete: {added} nouns added.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_nouns.py batches/your-nouns.json")
        sys.exit(1)
    import_nouns(sys.argv[1])
