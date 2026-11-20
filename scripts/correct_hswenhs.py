import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm

CORRECTIONS = {
    "-hswenhs": [
        ("íhswenhs", "1sg", "3m/i"),     # Page 42
        ("ráhswenhs", "3m", "3m/i"),     # Page 42
        ("yéhswenhs", "3f", "3m/i"),     # Page 42
        ("kónhswenhs", "1sg", "2sg"),    # Page 46
        ("ríhswenhs", "1sg", "3m"),      # Page 46
        ("étshswenhs", "2sg", "3m"),     # Page 46
    ]
}

def fix_db():
    app = create_app()
    with app.app_context():
        for root, forms in CORRECTIONS.items():
            verb = Verb.query.filter_by(root=root).first()
            if not verb: continue
            
            for target_form, correct_subj, correct_obj in forms:
                vf = VocabForm.query.filter_by(verb_id=verb.id, form=target_form).first()
                if vf:
                    print(f"Fixing {root} '{target_form}': -> {correct_subj}>{correct_obj}")
                    vf.subject = correct_subj
                    vf.object = correct_obj
                else:
                    print(f"Warning: Form '{target_form}' not found for {root}. The DB might have misspelled it.")
        
        db.session.commit()
        print("DB fixed.")

if __name__ == "__main__":
    fix_db()
