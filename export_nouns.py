import json
from app import app
from models import db, Vocab

with app.app_context():
    # Get all vocab that isn't linked to a lesson, or just get ALL vocab to be safe
    vocab_items = Vocab.query.all()
    
    export_data = []
    for v in vocab_items:
        export_data.append({
            "mohawk": v.mohawk,
            "english": v.english,
            "category": v.category,
            "prefix_color": v.prefix_color,
            "notes": v.notes
        })
        
    with open("batches/recovered_nouns.json", "w", encoding="utf-8") as f:
        json.dump({"vocab": export_data}, f, ensure_ascii=False, indent=2)
        
    print(f"Exported {len(export_data)} vocab items to batches/recovered_nouns.json")
