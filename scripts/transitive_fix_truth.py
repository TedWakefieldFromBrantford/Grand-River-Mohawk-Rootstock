import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db, Verb, VocabForm

# The Gospel Truth from Pages 46 & 40
# Format: { "root": [ ("form", "subject", "object") ] }
CORRECTIONS = {
    "-nòn:we's": [
        ("rakenòn:we's", "3m", "1sg"),       # Page 46: he -> me
        ("yesanòn:we's", "3pl.f", "2sg"),    # Page 46: she/s.o./they -> you
        ("ronwanòn:we's", "3pl.f", "3m"),    # Page 46: she/s.o./they -> him
    ],
    "-yenté:ri": [
        ("rakyenté:ri", "3m", "1sg"),        # Page 46: he -> me
        ("yesayenté:ri", "3pl.f", "2sg"),    # Page 46: she/s.o./they -> you
        ("ronwayenté:ri", "3pl.f", "3m"),    # Page 46: she/s.o./they -> him
    ],
    "-norónhkwa": [
        ("rakenorónhkwa", "3m", "1sg"),      # Page 46: he -> me
        ("yesanorónhkwa", "3pl.f", "2sg"),   # Page 46: she/s.o./they -> you
        ("ronwanorónhkwa", "3pl.f", "3m"),   # Page 46: she/s.o./they -> him
    ],
    "-hswenhs": [
        # Page 46: I -> you is kónhswenhs, NOT kontíhswenhs
        ("kónhswenhs", "1sg", "2sg"),
        # Page 42: I hate it is ikhswenhs
        ("ikhswenhs", "1sg", "3m/i"),
        # Page 42: he hates it is ráhswenhs
        ("ráhswenhs", "3m", "3m/i"),
        # Page 42: she hates it is yéhswenhs
        ("yéhswenhs", "3f", "3m/i"),
    ]
}

def fix_db():
    app = create_app()
    with app.app_context():
        for root, forms in CORRECTIONS.items():
            verb = Verb.query.filter_by(root=root).first()
            if not verb:
                print(f"Warning: Verb {root} not found.")
                continue
            
            for target_form, correct_subj, correct_obj in forms:
                vf = VocabForm.query.filter_by(verb_id=verb.id, form=target_form).first()
                if vf:
                    print(f"Fixing {root} '{target_form}': {vf.subject}>{vf.object} -> {correct_subj}>{correct_obj}")
                    vf.subject = correct_subj
                    vf.object = correct_obj
                else:
                    print(f"Warning: Form '{target_form}' not found for {root}.")
        
        db.session.commit()
        print("Database truths updated.")

if __name__ == "__main__":
    fix_db()
