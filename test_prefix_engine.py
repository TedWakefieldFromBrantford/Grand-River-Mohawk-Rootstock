# test_prefix_engine.py
import sqlite3
from prefix_engine import conjugate

def run_tests():
    print("Connecting to database...")
    conn = sqlite3.connect('./instance/mohawk.db')
    cursor = conn.cursor()

    # Get ALL forms for the 4 verbs we are currently testing
    cursor.execute("""
        SELECT v.root, vf.subject, vf.object, vf.form, vf.form_type
        FROM vocab_form vf
        JOIN verb v ON vf.verb_id = v.id
        WHERE v.root IN ('-nòn:we''s', '-yenté:ri', '-norónhkwa', '-hswenhs')
    """)
    rows = cursor.fetchall()

    passed = 0
    failed = 0

    print(f"Testing {len(rows)} forms...\n")

    for root, subject, obj, expected, form_type in rows:
        # Call our engine, passing the form_type!
        actual = conjugate(root, subject, obj, form_type=form_type)
        
        if actual == expected:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: {root} | {subject} -> {obj} ({form_type})")
            print(f"  Expected: {expected}")
            print(f"  Got:      {actual}")
            print("-" * 40)

    print(f"\nResults: {passed} Passed, {failed} Failed.")
    return failed

def test_prefix_engine_suite():
    """Pytest wrapper. Will fail if ANY form fails."""
    failures = run_tests()
    assert failures == 0, f"Prefix engine failed on {failures} forms."

if __name__ == "__main__":
    run_tests()
