# prefix_engine.py
from stem_classes import PREFIX_MATRIX, PURPLE_PREFIX_MATRIX
from reflexive_engine import REFLEXIVE_MATRIX, RECIPROCAL_MATRIX
from exceptions_engine import apply_exceptions

BASE_VOWELS = "aeiou"
VOWELS = "aeiouáéíóúàèìòù"
ACCENTS = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}

STEM_CLASS_BY_VOWEL = {
    "a": "A", "á": "A",
    "i": "I", "í": "I",
    "e": "E", "é": "E",
    "o": "O", "ó": "O",
}

def _is_vowel(char): return char.lower() in VOWELS
def is_consonant(char): return char.lower() not in VOWELS

def infer_stem_class(root):
    """Derive the stem class from the root's first letter.
    C-stem is the default (consonant-initial)."""
    clean = root.lstrip("-")
    if not clean:
        return "C"
    first = clean[0].lower()
    return STEM_CLASS_BY_VOWEL.get(first, "C")

def _engine_key(name):
    CANON_TO_ENGINE = {
        "3m/i": "3i", 
        "1pl.incl": "1pl.in", "1pl.excl": "1pl.ex",
        "1du.incl": "1du.in", "1du.excl": "1du.ex",
        "1du": "1du.in", "1pl": "1pl.in", 
    }
    return CANON_TO_ENGINE.get(name, name)

def accent_last_vowel(word):
    chars = list(word)
    for i in range(len(chars)-1, -1, -1):
        if _is_vowel(chars[i]):
            if chars[i].lower() in BASE_VOWELS:
                chars[i] = ACCENTS[chars[i].lower()]
            return "".join(chars)
    return word

def apply_phonology(prefix, root, subject, obj, is_negated=False, form_type="transitive"):
    if not prefix: return ""
        
    clean_root = root.lstrip("-")
    first_letter = clean_root[0].lower()
    
    # --- Rule 11: take- mutations ---
    if prefix.startswith("take"):
        if is_negated: prefix = "hsk" + prefix[4:]
        elif first_letter in ["h", "k", "y"]: prefix = "tak" + prefix[4:]

    # --- Rule 6 & 7: Vowel drop ---
    if prefix.endswith(("a", "o")) and first_letter in ["a", "i"]:
        prefix = prefix[:-1]

    # --- THE -hswenhs CONTRACTIONS ---
    if clean_root == "hswenhs":
        HSWENHS_MAP = {
            "ken": "ik", "hsen": "í", "teni": "tení", "yakeni": "yakení",
            "seni": "sení", "hni": "hní", "keni": "kení", "tewa": "tewá",
            "yakwa": "yakwá", "sewa": "sewá",
            "ka": "ká", "ra": "rá", "sa": "sá", "ye": "yé", "ro": "ró",
            "wake": "wák", "rake": "rák", "yesa": "yesá", "yako": "yakó",
            "hshako": "hshakó", "yonke": "yónk", "yontate": "yontáth", "take": "ták",
            "hya": "yá", "hshe": "hshé", "etshe": "étsh", "hse": "í", 
            "ke": "ík", "kwa": "kwá", "ky": "kí", "kw": "kwé",
            "yakw": "yakwé", "tew": "tewé", "sew": "sewé",
            "ronwa": "ronwá", "shakoti": "shakotí", "yakoti": "yakotí"
        }
        
        if subject == "1du.in": prefix = "yakeni"
        elif subject == "1du.ex": prefix = "teni"
        elif subject == "1pl.in": prefix = "yakwa"
        elif subject == "1pl.ex": prefix = "tewa"

        if prefix in HSWENHS_MAP:
            contracted = HSWENHS_MAP[prefix]
            if contracted.endswith("h") and clean_root.startswith("h"):
                clean_root = clean_root[1:]
            return contracted + clean_root
        
        if subject == "1sg" and obj == "3i":
            return "ik" + clean_root
            
        return accent_last_vowel(prefix) + clean_root

    # --- Pre-y Reduction for ken/hsen ---
    if first_letter == "y":
        if prefix == "ken": 
            prefix = "ky"
            clean_root = clean_root[1:]
        elif prefix == "hsen": 
            prefix = "hsy"
            clean_root = clean_root[1:]
    
    # --- Reflexive Epenthesis ---
    if form_type in ["reflexive", "reciprocal"]:
        if first_letter == "y":
            if prefix == "ronatate": prefix = "rontate"
            elif prefix == "kontatate": prefix = "kontate"
        
        if prefix.endswith("tate") and first_letter == "y":
            prefix = prefix[:-1]  # tate -> tat
        elif prefix.startswith("yon") and prefix.endswith("tate") and first_letter == "n":
            prefix = prefix[:-4] + "atate" 
        
        if prefix.startswith("tyatate") and first_letter == "n":
            prefix = prefix[1:]
            

    # --- Transitive 3f Epenthesis ---
    if subject == "3f" and obj == "3f" and form_type == "transitive":
        if prefix == "yontate" and first_letter == "y":
            prefix = prefix[:-1]
        if prefix == "yontate" and first_letter == "n":
            prefix = "yonate"

    # --- Weak 'e' drops ---
    if prefix in ["ke", "hse"] and first_letter in ["h", "y", "k"]: prefix = prefix[:-1]
    if prefix == "etshe":
        if first_letter == "y": prefix = "ets"
        elif first_letter in ["h", "k"]: prefix = "etsh"
    if first_letter == "y" and prefix in ["wake", "rake", "yonke"]: prefix = prefix[:-1]

    # --- n + y drop (only for 'yon') ---
    if prefix == "yon" and first_letter == "y":
        prefix = prefix[:-1]

    # --- De-gemination ---
    if prefix.endswith("n") and clean_root.startswith("n"):
        if prefix in ["ken", "hsen", "yon"]:
            clean_root = clean_root[1:]

    # --- Special case for -norónhkwa ---
    if clean_root == "norónhkwa":
        if prefix == "sa": return "saninorónhkwa"
        if prefix == "ro"and subject == "3i": return "roninorónhkwa"
        if prefix == "yon": return "yonorónhkwa"

    return prefix + clean_root

def apply_negation(word, subject, obj, first_letter, stem_class):
    if subject == "2sg" and obj == "1sg":
        if first_letter in ["h", "k"]: word = "yah tehsek" + word[3:]
        elif first_letter == "y": word = "yah tehsk" + word[3:]
        else: word = "yah tehs" + word[2:]
    else:
        if word.startswith("i"): word = "yah té" + word[1:]
        elif word.startswith("te"): word = "yah th'" + word[2:]
        else: word = "yah te" + word
    return word

def _get_prefix(subject, obj, form_type, stem_class):
    if form_type == "reflexive": 
        if subject == "3n": subject = "3i"
        if obj =="3n": obj = "3i"
        if obj == "1du": obj = "1du.ex" if subject.startswith("1du.ex") else "1du.in"
        if obj == "1pl": obj = "1pl.ex" if subject.startswith("1pl.ex") else "1pl.in"
        
        row = REFLEXIVE_MATRIX.get((subject, obj), {})
        if not row:
            row = REFLEXIVE_MATRIX.get((subject, subject), {})
        return row.get(stem_class)
        
    if form_type == "reciprocal": 
        if obj == "1du": obj = "1du.ex" if subject.startswith("1du.ex") else "1du.in"
        if obj == "1pl": obj = "1pl.ex" if subject.startswith("1pl.ex") else "1pl.in"
        
        row = RECIPROCAL_MATRIX.get((subject, obj), {})
        if not row:
            row = RECIPROCAL_MATRIX.get((subject, subject), {})
        return row.get(stem_class)
    
    prefix = PURPLE_PREFIX_MATRIX.get((subject, obj), {}).get(stem_class)
    if prefix: return prefix
    return PREFIX_MATRIX.get((subject, obj), {}).get(stem_class)

def conjugate(root, subject, obj, is_negated=False, form_type="transitive", stem_class=None):
    """Generates a verb form using morphology + phonology + exceptions."""
    if stem_class is None:
        stem_class = infer_stem_class(root)
    
    eng_subject = _engine_key(subject)
    eng_obj = _engine_key(obj) 
    
    prefix = _get_prefix(eng_subject, eng_obj, form_type, stem_class)
    if not prefix: 
        return f"[NO RULE: {subject}->{obj} ({form_type})]"

    word = apply_phonology(prefix, root, eng_subject, eng_obj, is_negated, form_type)
    
    if is_negated:
        first_letter = root.lstrip("-")[0].lower()
        word = apply_negation(word, eng_subject, eng_obj, first_letter, stem_class)
    
    # Last step: apply the documented exceptions layer
    return apply_exceptions(root, subject, obj, form_type, word)
