from datetime import datetime
from models import db, Session, Attempt

def start_session(lesson_id, mode="practice", user_id=None, drill_mix=None):
    s = Session(
        lesson_id=lesson_id,
        mode=mode,
        user_id=user_id,
        drill_mix_json=drill_mix or {},
        started_ts=datetime.utcnow(),
    )
    db.session.add(s)
    db.session.commit()
    return s.id

def record(session_id, item_id, result, duration_ms=0):
    db.session.add(Attempt(
        session_id=session_id,
        item_id=item_id,
        result=result,
        duration_ms=duration_ms,
        ts=datetime.utcnow(),
    ))
    db.session.commit()

def summary(session_id):
    rows = Attempt.query.filter_by(session_id=session_id).all()
    hits   = sum(1 for r in rows if r.result == 2)
    nears  = sum(1 for r in rows if r.result == 1)
    misses = sum(1 for r in rows if r.result == 0)
    return {"total": len(rows), "hits": hits, "nears": nears, "misses": misses}
