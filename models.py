from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Lesson(db.Model):
    __tablename__ = "lesson"
    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text, default="")

class Vocab(db.Model):
    __tablename__ = "vocab"
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=True)
    mohawk = db.Column(db.String, nullable=False)
    english = db.Column(db.String, nullable=False)
    category = db.Column(db.String, default="")          # color / animal / household
    class_or_stem = db.Column(db.String, default="")      # red / blue / purple
    notes = db.Column(db.Text, default="")

class Verb(db.Model):
    __tablename__ = "verb"
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=True)
    root = db.Column(db.String, nullable=False)
    gloss = db.Column(db.String, nullable=False)
    forms_json = db.Column(db.JSON, nullable=False)      # {"1sg": "...", "3f": "...", ...}
    notes = db.Column(db.Text, default="")

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=True)
    qtype = db.Column(db.String, nullable=False)         # translate / verb / sentence
    payload_json = db.Column(db.JSON, nullable=False)    # free-form per qtype

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)       # dormant: always NULL in year one
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=True)
    mode = db.Column(db.String, nullable=False, default="practice")  # practice / quiz
    drill_mix_json = db.Column(db.JSON, default=dict)    # {"translate": 10, "verb": 5, ...}
    started_ts = db.Column(db.DateTime, nullable=False)
    ended_ts = db.Column(db.DateTime, nullable=True)

class Attempt(db.Model):
    __tablename__ = "attempt"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("session.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    result = db.Column(db.Integer, nullable=False)        # 0 miss / 1 near / 2 hit
    duration_ms = db.Column(db.Integer, default=0)
    ts = db.Column(db.DateTime, nullable=False)


# ==========================================
# NEW SCHEMA V2 TABLES
# ==========================================

class VocabForm(db.Model):
    __tablename__ = "vocab_form"
    id = db.Column(db.Integer, primary_key=True)
    
    # Either link to a Vocab word OR a Verb root
    vocab_id = db.Column(db.Integer, db.ForeignKey("vocab.id"), nullable=True)
    verb_id = db.Column(db.Integer, db.ForeignKey("verb.id"), nullable=True)
    
    form = db.Column(db.String, nullable=False)
    form_type = db.Column(db.String, default="citation")
    subject = db.Column(db.String, default="")
    object = db.Column(db.String, default="")
    english_gloss = db.Column(db.String, default="")
    attrs_json = db.Column(db.JSON, default=dict)
    notes = db.Column(db.Text, default="")
    source_batch = db.Column(db.String, default="")
    source_page = db.Column(db.String, default="")

    # Access the parent verb or vocab easily (e.g., form.verb.root)
    verb = db.relationship("Verb", backref="forms")
    vocab = db.relationship("Vocab", backref="forms")

    __table_args__ = (
        CheckConstraint('(vocab_id IS NOT NULL AND verb_id IS NULL) OR (vocab_id IS NULL AND verb_id IS NOT NULL)', 
                        name='check_vocab_or_verb'),
    )

class Example(db.Model):
    __tablename__ = "example"
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    vocab_id = db.Column(db.Integer, db.ForeignKey("vocab.id"), nullable=True)
    verb_id = db.Column(db.Integer, db.ForeignKey("verb.id"), nullable=True)
    
    mohawk_text = db.Column(db.Text, nullable=False)
    english_text = db.Column(db.Text, default="")
    notes = db.Column(db.Text, default="")
    source_batch = db.Column(db.String, default="")

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class VocabTag(db.Model):
    __tablename__ = "vocab_tag"
    vocab_id = db.Column(db.Integer, db.ForeignKey("vocab.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)
class VerbTag(db.Model):
    __tablename__ = "verb_tag"
    verb_id = db.Column(db.Integer, db.ForeignKey("verb.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)

class VocabFormTag(db.Model):
    __tablename__ = "vocab_form_tag"
    vocab_form_id = db.Column(db.Integer, db.ForeignKey("vocab_form.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)

class Rule(db.Model):
    __tablename__ = "rule"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True) # e.g., "negation", "yes_no_question"
    description = db.Column(db.Text, default="")
    # How to transform it. We'll use a JSON structure.
    # Example: {"prefix": "yah te", "strip_initial": "i"} 
    # or: {"prefix": "ken ", "suffix": "?", "word_order": "verb_first"}
    transform_json = db.Column(db.JSON, nullable=False)
class SentenceTemplate(db.Model):
    __tablename__ = "sentence_template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) # e.g. "Transitive Statement"
    # The order of words in Mohawk vs English
    # e.g. {"mohawk": ["verb", "object"], "english": ["subject", "verb", "object"]}
    structure_json = db.Column(db.JSON, nullable=False)
