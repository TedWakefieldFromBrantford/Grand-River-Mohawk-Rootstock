# routes.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import db, Lesson, Vocab, Verb, Item, VocabForm
from compare import compare, FEEDBACK
import session as sess
from questions import REGISTRY

# Create a Blueprint. This is just a collection of routes.
bp = Blueprint('main', __name__)

@bp.route("/")
def index():
    lessons = Lesson.query.order_by(Lesson.week_number).all()
    return render_template("base.html", body=render_template("index.html", lessons=lessons))

@bp.route("/quiz/<int:lesson_id>")
def quiz(lesson_id):
    mode = request.args.get("mode", "practice")
    vocab = Vocab.query.filter_by(lesson_id=lesson_id).all()
    if not vocab:
        return "No vocab in this lesson yet.", 404
    questions = REGISTRY["translate"].generate(lesson_id, vocab, n=len(vocab))
    sid = sess.start_session(lesson_id, mode=mode,
                             drill_mix={"translate": len(questions)})
    return render_template("base.html",
        body=render_template("quiz.html", questions=questions,
                             session_id=sid, mode=mode))

@bp.route("/attempt", methods=["POST"])
def attempt():
    data = request.get_json()
    expected = data["answer"]
    given = data.get("given", "")
    result, detail = compare(expected, given)
    sess.record(int(data["session_id"]), int(data["item_id"]), result,
                int(data.get("duration_ms", 0)))
    msg = FEEDBACK[result].format(expected=expected)
    return jsonify({"result": result, "message": msg, "detail": detail,
                    "expected": expected})

@bp.route("/summary/<int:session_id>")
def summary(session_id):
    s = sess.summary(session_id)
    return render_template("base.html", body=render_template("summary.html", s=s))

# --- Dual-mode Admin Route ---
@bp.route("/admin/edit", methods=["GET", "POST"])
@bp.route("/admin/edit/lesson/<int:lesson_id>", methods=["GET", "POST"])
def edit_lesson(lesson_id=None):
    lesson = None
    if lesson_id is not None:
        lesson = Lesson.query.get_or_404(lesson_id)
        vocab = Vocab.query.filter_by(lesson_id=lesson_id).all()
        verbs = Verb.query.filter_by(lesson_id=lesson_id).all()
    else:
        # "Edit Everything" mode (no lesson filter)
        vocab = Vocab.query.all()
        verbs = Verb.query.all()

    if request.method == "POST":
        # --- 1. VOCAB UPSERT ---
        mohawk_list = request.form.getlist("mohawk")
        english_list = request.form.getlist("english")
        category_list = request.form.getlist("category")
        class_list = request.form.getlist("class or stem")
        vocab_notes_list = request.form.getlist("vocab_notes") 

        existing_vocab = {v.mohawk.strip(): v for v in vocab}
        
        for m, e, c, cl, n in zip(mohawk_list, english_list, category_list, class_list, vocab_notes_list):
            m = m.strip()
            if not m or not e.strip():
                continue
            if m in existing_vocab:
                v = existing_vocab[m]
                v.english = e
                v.category = c
                v.class_or_stem = cl
                v.notes = n
                del existing_vocab[m]
            else:
                db.session.add(Vocab(lesson_id=lesson_id, mohawk=m, english=e, category=c, class_or_stem=cl, notes=n))

        # --- 2. VERB UPSERT ---
        verb_ids = request.form.getlist("verb_id")
        verb_roots = request.form.getlist("verb_root")
        verb_glosses = request.form.getlist("verb_gloss")
        verb_notes = request.form.getlist("verb_notes")

        for i in range(len(verb_roots)):
            root = verb_roots[i].strip()
            if not root:
                continue
            
            v_id = verb_ids[i] if i < len(verb_ids) else ""
            gloss = verb_glosses[i].strip()
            notes = verb_notes[i].strip()

            if v_id:
                v = Verb.query.get(int(v_id))
                if v:
                    v.root = root
                    v.gloss = gloss
                    v.notes = notes
                    # Don't overwrite lesson_id if we are in "edit all" mode
                    if lesson_id:
                        v.lesson_id = lesson_id
            else:
                db.session.add(Verb(lesson_id=lesson_id, root=root, gloss=gloss, notes=notes, forms_json={}))

        db.session.commit() # Commit verbs so they get IDs for the forms dropdown!

        # --- 3. VOCAB FORM UPSERT ---
        form_ids = request.form.getlist("form_id")
        form_verb_ids = request.form.getlist("form_verb_id")
        form_mohawks = request.form.getlist("form_mohawk")
        form_types = request.form.getlist("form_type")
        form_subjects = request.form.getlist("form_subject")
        form_objects = request.form.getlist("form_object")
        form_glosses = request.form.getlist("form_gloss")
        form_notes = request.form.getlist("form_notes") # NEW: Parse notes

        for i in range(len(form_mohawks)):
            f_id = form_ids[i] if i < len(form_ids) else ""
            f_verb_id = form_verb_ids[i]
            f_mohawk = form_mohawks[i].strip()
            
            if not f_mohawk or not f_verb_id:
                continue
            
            notes = form_notes[i] if i < len(form_notes) else ""

            if f_id:
                vf = VocabForm.query.get(int(f_id))
                if vf:
                    vf.verb_id = int(f_verb_id)
                    vf.form = f_mohawk
                    vf.form_type = form_types[i]
                    vf.subject = form_subjects[i]
                    vf.object = form_objects[i]
                    vf.english_gloss = form_glosses[i]
                    vf.notes = notes # NEW: Save notes
            else:
                vf = VocabForm(
                    verb_id=int(f_verb_id),
                    form=f_mohawk,
                    form_type=form_types[i],
                    subject=form_subjects[i],
                    object=form_objects[i],
                    english_gloss=form_glosses[i],
                    notes=notes, # NEW: Save notes
                    source_batch="manual"
                )
                db.session.add(vf)

        db.session.commit()
        
        # Redirect to the correct place based on mode
        if lesson_id:
            return redirect(url_for("main.edit_lesson", lesson_id=lesson_id))
        return redirect(url_for("main.edit_lesson"))

    # --- GET Request ---
    if lesson_id:
        forms = VocabForm.query.join(Verb).filter(Verb.lesson_id == lesson_id).all()
    else:
        forms = VocabForm.query.all()
        
    return render_template("base.html", body=render_template(
        "admin_edit.html", lesson=lesson, vocab=vocab, verbs=verbs, forms=forms
    ))
