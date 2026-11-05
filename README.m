# Grand River Mohawk Rootstock

A study tool for learners of Kanien'kéha (Mohawk), built on the
Onkwawenna Kentyohkwa 1st Year Program curriculum.

**This is a work in progress, mirroring my own learning journey.** 

Rootstock is *not* a chatbot, an AI tutor, or a replacement for a
speaker or teacher. It is a **structured, human-curated corpus** of
vocabulary, verb paradigms, and example sentences, paired with a
drill engine that generates flashcards, quizzes, and tests from that
corpus. Every entry is traceable to a textbook page or a vetted
source. When the corpus is wrong, the drill is wrong — which is why
provenance notes are built into the data model from day one.

## Rebuild the database from scratch

The database is disposable scaffolding. It can be rebuilt at any time from the JSON files in `batches/`:

```bash
# 1. Delete the existing DB
rm -f instance/mohawk.db

# 2. Create the tables
python -c "from app import app; from models import db; app.app_context().push(); db.create_all(); print('DB rebuilt')"

# 3. Import verbs/forms
python import_batch.py batches/unit2_like_know_love_hate.json

# 4. Import nouns
python import_nouns.py batches/recovered_nouns.json
