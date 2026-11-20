# grammar.py

# Lexical exceptions: forms that don't follow a generalizable rule.
# Each entry must have a corresponding test in test_grammar.py.
# Source: Onkwawenna Kentyohkwa 1st Year Program, p. 40, p. 51, p. 75.
NEGATION_EXCEPTIONS = {
    # p. 40: 'i' drops and 'e' takes an acute accent (pre-composed U+00E9).
    "ikhswenhs": "yah tékhswenhs",
}


def apply_negation(base_form):
    """
    Negation rules, verified against the textbook.

    p. 40:  Default is 'yah te' + form.
    p. 40:  'ikhswenhs' -> 'yah tékhswenhs' (lexical exception, see NEGATION_EXCEPTIONS).
    p. 75:  Any form beginning with 'te' (dual prefix) -> 'yah tha' + form.
            Exceptions: 'tewa-' and 'teni-' take normal 'yah te'.
    p. 51:  'tak-' prefix (you-to-me) becomes 'yah tehs[k]-' before y/h/k,
            and 'take-' becomes 'yah tehske-'.
    """
    if base_form in NEGATION_EXCEPTIONS:
        return NEGATION_EXCEPTIONS[base_form]

    # p. 75: te- dual prefix rule. tewa- and teni- are exceptions.
    if base_form.startswith("te") and not base_form.startswith(("tewa", "teni")):
        return "yah tha'" + base_form

    # p. 51: tak- prefix (you -> me) becomes tehsk-/tehske-.
    if base_form.startswith("take"):
        return "yah tehs" + base_form[3:]   # take- -> tehske-
    if base_form.startswith("tak"):
        return "yah tehs" + base_form[2:]   # tak-  -> tehsk-

    return "yah te" + base_form


# Particle categories, sourced from Unit 1 & Unit 3.
PARTICLES = {
    # Unit 1 (pp. 23-26)
    "ken":        {"gloss": "? (2nd position)",        "page": 23},
    "yah":        {"gloss": "no / not",                "page": 24},
    "ó:ni":       {"gloss": "also / too",              "page": 23},
    "nok":        {"gloss": "and",                     "page": 23},
    "tahn[on]":   {"gloss": "and / and besides",       "page": 23},
    "é:so":       {"gloss": "a lot",                   "page": 24},
    "sénha":      {"gloss": "more",                    "page": 24},
    "sótsi":      {"gloss": "too much",                "page": 26},
    "ohstón:ha":  {"gloss": "a little",                "page": 24},
    "akwá:kon":   {"gloss": "everyone / everything",   "page": 23},
    "wáhi":       {"gloss": "isn't it? (tag question)", "page": 23},
    "ne":         {"gloss": "the / the one who",       "page": 26},
    "tsi":        {"gloss": "that / there / when",     "page": 25},
    "thí:ken":    {"gloss": "that",                    "page": 26},
    "kí:ken":     {"gloss": "this",                    "page": 26},
    
    # Unit 3 (pp. 96-97)
    "né:'e tsi":  {"gloss": "because",                  "page": 96},
    "ne karihón:ni": {"gloss": "that's why",            "page": 96},
    "ó:nen":      {"gloss": "now / already",            "page": 97},
    "kári:wes":   {"gloss": "a long time",              "page": 97},
    "nikarihwéhsha": {"gloss": "a short time",          "page": 97},
    "nyá:wen":    {"gloss": "thank you / thanks",       "page": 97},
    "khá:re ó:nen": {"gloss": "finally",                "page": 97},
    "nonwén:ton": {"gloss": "ever",                     "page": 97},
    "yah nonwén:ton": {"gloss": "never",                "page": 97},
}


class SentenceBuilder:
    """
    Assembles a Mohawk sentence from parts, respecting textbook word order.

    Slot order (verified against Unit 1-2 examples):
      1. Pre-verbal particles (yah, é:so, sénha, ...)
      2. The conjugated verb
      3. The object, marked with 'ne'
      4. Trailing particles (ó:ni, wáhi)
    """

    def __init__(self, verb_form, object_noun=None):
        self.verb_form = verb_form
        self.object_noun = object_noun
        self.pre = []
        self.post = []

    def with_pre(self, particle):
        """Add a pre-verbal particle. Returns self for chaining."""
        self.pre.append(particle)
        return self

    def with_post(self, particle):
        """Add a trailing particle. Returns self for chaining."""
        self.post.append(particle)
        return self

    def build(self):
        parts = []
        parts.extend(self.pre)
        parts.append(self.verb_form)
        if self.object_noun:
            parts.append(f"ne {self.object_noun}")
        parts.extend(self.post)
        return " ".join(parts)


# --- Standalone Transformation Functions ---

def make_question(sentence):
    """
    Injects 'ken' as the second word of the sentence.
    Textbook rule: formulate your sentence so ken is the second word.
    """
    words = sentence.split()
    
    # If it's a one-word sentence, ken just goes after it
    if len(words) == 1:
        return f"{words[0]} ken?"
        
    # Insert 'ken' at index 1 (the second position)
    words.insert(1, "ken")
    
    result = " ".join(words)
    # Capitalize the first letter and add a question mark
    return result[0].upper() + result[1:] + "?"
