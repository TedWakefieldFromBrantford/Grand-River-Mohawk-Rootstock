# exceptions_engine.py
"""
Known textbook exceptions that the rule-based generator cannot produce.
Every entry is (root, subject, object, form_type) -> exact_form.
Call this AFTER generating a word; if the key exists here, it overrides.

MAINTENANCE:
- Every entry should be a true linguistic irregular, NOT a database ambiguity.
- Database ambiguities get fixed with SQL, not exceptions.
- When you extract a pattern into a rule, remove the matching entries.
"""

KNOWN_EXCEPTIONS = {
    # ==========================================
    # -yenté:ri specific edges
    # ==========================================
    # 1sg/2sg -> 3m/i use ky-/hsy- before y (root-specific reduction)
    ("-yenté:ri", "1sg", "3m/i", "transitive"): "kyenté:ri",
    ("-yenté:ri", "2sg", "3m/i", "transitive"): "hsyenté:ri",

    # Reflexive with 3i subject uses kataty- (not wataty-)
    ("-yenté:ri", "3i", "3m/i", "reflexive"): "katatyenté:ri",

    # Reciprocal 3pl uses hon-/kon- (not honata-/konata-)
    ("-yenté:ri", "3pl.m", "3pl.m", "reciprocal"): "tehontatyenté:ri",
    ("-yenté:ri", "3pl.f", "3pl.f", "reciprocal"): "tekontatyenté:ri",

    # ==========================================
    # -hswenhs citation
    # ==========================================
    # 3i -> 3i uses yó- for this root (matrix says ka-)
    # TODO: verify against textbook — this may be a DB typo
    ("-hswenhs", "3i", "3i", "citation"): "yóhswenhs",

    # -norónhkwa 3m -> 3f uses hshaka (a, not o) before n
    ("-norónhkwa", "3m", "3f", "transitive"): "hshakanorónhkwa",
}

def apply_exceptions(root, subject, obj, form_type, generated_form):
    """If this exact form is a known exception, return it. Otherwise, return the generated form."""
    key = (root, subject, obj, form_type)
    if key in KNOWN_EXCEPTIONS:
        return KNOWN_EXCEPTIONS[key]
    return generated_form
