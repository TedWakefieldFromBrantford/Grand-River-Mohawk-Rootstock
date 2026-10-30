import unicodedata

FEEDBACK = {
    2: "Yes.",
    1: "That's the word — the accents need adjusting.",
    0: "Not this one. The answer is {expected}.",
}

_APOSTROPHES = "'\u2019\u02bc\u02bb"

def _nfc(s):
    return unicodedata.normalize("NFC", s).strip()

def _collapse_ws(s):
    return " ".join(s.split())

def _norm_apostrophes(s):
    for ch in _APOSTROPHES:
        s = s.replace(ch, "'")
    return s

def _strip_marks(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c))

def compare(expected, given):
    """Return (result:int, detail:dict).
    result: 2 hit, 1 near (only accents/apostrophes differ), 0 miss."""
    e = _collapse_ws(_nfc(expected))
    g = _collapse_ws(_nfc(given))

    if e == g:
        return 2, {}

    # Layer 2: apostrophe variant
    if _norm_apostrophes(e) == _norm_apostrophes(g):
        return 1, {"reason": "apostrophe"}

    # Layer 3: diacritic-insensitive
    e_plain, g_plain = _strip_marks(e), _strip_marks(g)
    if e_plain == g_plain:
        return 1, {"reason": "accent",
                   "diff_positions": _diff_positions(e, g)}

    return 0, {"expected_display": e}

def _diff_positions(expected, given):
    """Character indices where the marked forms differ. For UI highlighting."""
    out = []
    n = min(len(expected), len(given))
    for i in range(n):
        if expected[i] != given[i]:
            out.append(i)
    if len(expected) != len(given):
        out.append(min(len(expected), len(given)))
    return out
