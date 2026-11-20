"""Throwaway: inspect distinct subject/object values for the quiz UI.
Run from project root:  python scripts/db_check.py [path/to/db]
"""
import sqlite3, sys, glob, os

def find_db():
    if len(sys.argv) > 1:
        return sys.argv[1]
    hits = glob.glob("*.db") + glob.glob("*.sqlite") + glob.glob("*.sqlite3")
    hits += glob.glob("**/*.db", recursive=True) + glob.glob("**/*.sqlite*", recursive=True)
    hits = [h for h in hits if "test" not in h.lower()]
    if not hits:
        sys.exit("No .db found. Pass a path explicitly.")
    if len(hits) > 1:
        print("Multiple DBs found, using first:", hits[0])
    return hits[0]

def q(con, sql, label):
    print(f"\n--- {label} ---")
    try:
        rows = con.execute(sql).fetchall()
    except sqlite3.Error as e:
        print(f"  !! {e}  (sql: {sql})")
        return
    if not rows:
        print("  (no rows)")
        return
    for r in rows:
        print("  ", r)

def main():
    db = find_db()
    print("DB:", os.path.abspath(db))
    con = sqlite3.connect(db)

    # What tables exist?
    q(con, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", "TABLES")

    # The four things the UI needs
    q(con, "SELECT category, COUNT(*) FROM Vocab GROUP BY category ORDER BY category",
      "Vocab.categories")
    q(con, "SELECT id, gloss FROM Verb ORDER BY gloss", "Verb.gloss (for checkboxes)")
    q(con, "SELECT DISTINCT subject FROM VocabForm ORDER BY subject",
      "distinct VocabForm.subject")
    q(con, "SELECT DISTINCT object  FROM VocabForm ORDER BY object",
      "distinct VocabForm.object")

    # Sanity: how many forms per (subject, object)?
    q(con, """SELECT subject, object, COUNT(*) FROM VocabForm
              GROUP BY subject, object ORDER BY subject, object""",
      "form count per subject/object pair")

if __name__ == "__main__":
    main()
