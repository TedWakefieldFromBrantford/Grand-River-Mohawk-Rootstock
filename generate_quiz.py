import random
import sys
from flask import Flask
from models import db, Verb, VocabForm, Vocab
from config import Config
from grammar import apply_negation, SentenceBuilder

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def generate_prompt(mode="random"):
    with app.app_context():
        print("\n--- Grand River Mohawk Quiz Generator ---")

        if mode == "random":
            mode = random.choice(["verb_form", "sentence", "negated_sentence"])

        if mode == "verb_form":
            target = random.choice(VocabForm.query.all())
            prompt_english = target.english_gloss
            answer = target.form
            root = target.verb.root if target.verb else "n/a"
            notes = (
                f"(Root: {root} | Type: {target.form_type} | "
                f"Subj: {target.subject} | Obj: {target.object})"
            )

        elif mode in ["sentence", "negated_sentence"]:
            verb_gloss = random.choice(["like", "know", "love", "hate"])
            verb = Verb.query.filter_by(gloss=verb_gloss).first()
            if not verb:
                print(f"No verb found for gloss '{verb_gloss}'. Aborting.")
                return

            form = VocabForm.query.filter_by(
                verb_id=verb.id,
                form_type="transitive",
                subject="3f",
                object="3m/i",
            ).first()
            noun = random.choice(Vocab.query.filter_by(category="animal").all())

            if not form or not noun:
                print("Missing form or noun. Aborting.")
                return

            if mode == "sentence":
                prompt_english = f"She {verb_gloss}s the {noun.english}."
                answer = SentenceBuilder(form.form, object_noun=noun.mohawk).build()
            else:
                negated = apply_negation(form.form)
                prompt_english = f"She doesn't {verb_gloss} the {noun.english}."
                answer = SentenceBuilder(negated, object_noun=noun.mohawk).build()

            notes = f"(verb={form.form}, noun={noun.mohawk})"

        else:
            print(f"Unknown mode: {mode}")
            return

        print(f"\n[{mode.replace('_', ' ').title()}]")
        print("Translate this to Mohawk:")
        print(f"English: {prompt_english}")

        input("\nPress Enter to see the answer...")

        print(f"\nAnswer: {answer}")
        print(notes)
        print("-" * 40)


if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "random"
    generate_prompt(mode_arg)
