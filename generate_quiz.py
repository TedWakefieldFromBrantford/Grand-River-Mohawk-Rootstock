import random
from flask import Flask
from models import db, Verb, VocabForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def generate_prompt():
    with app.app_context():
        # Pick a random form from the database
        forms = VocabForm.query.all()
        if not forms:
            print("No forms in DB yet!")
            return

        target = random.choice(forms)
        
        # We want the user to translate the English gloss to Mohawk
        print("\n--- Mohawk Quiz Generator ---")
        print(f"Translate this to Mohawk:")
        print(f"English: {target.english_gloss}")
        
        input("Press Enter to see the answer...")
        
        print(f"Answer: {target.form}")
        print(f"(Root: {target.verb.root} | Type: {target.form_type} | Subj: {target.subject} | Obj: {target.object})")
        print("-" * 30)

if __name__ == "__main__":
    generate_prompt()
