import random

def generate(lesson_id, vocab_rows, direction="en2mo", n=1):
    """Return n translation questions.
    vocab_rows: list of Vocab model rows for the lesson."""
    rng = random.Random()
    picked = rng.sample(vocab_rows, min(n, len(vocab_rows)))
    out = []
    for v in picked:
        if direction == "en2mo":
            prompt, answer = v.english, v.mohawk
        else:
            prompt, answer = v.mohawk, v.english
        out.append({
            "qtype": "translate",
            "prompt": prompt,
            "answer": answer,
            "hint": v.prefix_color or "",
        })
    return out
