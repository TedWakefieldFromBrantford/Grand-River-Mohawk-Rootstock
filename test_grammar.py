# test_grammar.py
from grammar import apply_negation

def test_default_negation():
    assert apply_negation("kenòn:we's") == "yah tekenòn:we's"

def test_i_dropping():
    assert apply_negation("ikhswenhs") == "yah tékhswenhs"

def test_te_exception():
    assert apply_negation("teyakyatatyenté:ri") == "yah tha'teyakyatatyenté:ri"

if __name__ == "__main__":
    test_default_negation()
    test_i_dropping()
    test_te_exception()
    print("All grammar tests passed.")

def test_default_negation():
    assert apply_negation("kenòn:we's") == "yah tekenòn:we's"

def test_ikhswenhs_exception():
    # p. 40: must use pre-composed é (U+00E9), never combining U+0301.
    result = apply_negation("ikhswenhs")
    assert result == "yah t\u00e9khswenhs"
    assert "\u0301" not in result  # guard against the combining-accent regression

def test_te_dual_prefix():
    # p. 75
    assert apply_negation("teyakyatatyenté:ri") == "yah tha'teyakyatatyenté:ri"

def test_tewa_is_exception():
    # p. 40 footnote: tewa- takes normal yah te.
    assert apply_negation("tewakshsenna:ser") == "yah te" + "tewakshsenna:ser"

def test_teni_is_exception():
    # p. 40 footnote: teni- takes normal yah te.
    assert apply_negation("teniyohserá:ke") == "yah te" + "teniyohserá:ke"

def test_take_prefix():
    # p. 51: take- -> tehske-
    assert apply_negation("takenòn:we's") == "yah tehskenòn:we's"

def test_tak_prefix():

    # p. 51: tak- -> tehsk-
    assert apply_negation("takwayenté:ri") == "yah tehskwayenté:ri"

def test_reflexive():
    assert apply_negation("katatenòn:we's") == "yah tekatatenòn:we's"


# --- SentenceBuilder tests ---

def test_builder_simple():
    s = SentenceBuilder("yakonòn:we's", object_noun="érhar").build()
    assert s == "yakonòn:we's ne érhar"

def test_builder_negated():
    verb = apply_negation("yakonòn:we's")
    s = SentenceBuilder(verb, object_noun="érhar").build()
    assert s == "yah teyakonòn:we's ne érhar"

def test_builder_with_pre_particle():
    s = SentenceBuilder("yakonòn:we's", object_noun="érhar").with_pre("é:so").build()
    assert s == "é:so yakonòn:we's ne érhar"

def test_builder_with_post_particle():
    s = SentenceBuilder("yakonòn:we's", object_noun="érhar").with_post("ó:ni").build()
    assert s == "yakonòn:we's ne érhar ó:ni"

def test_builder_chaining_is_order_preserving():
    s = (SentenceBuilder("yakonòn:we's", object_noun="érhar")
         .with_pre("yah").with_pre("é:so").with_post("ó:ni").build())
    assert s == "yah é:so yakonòn:we's ne érhar ó:ni"

def test_particles_have_page_cites():
    # Provenance gate: no particle ships without a textbook page.
    for k, v in PARTICLES.items():
        assert "page" in v and isinstance(v["page"], int)

def test_ken_second_word():
    # p. 97 example: "Nonwén:ton ken sanyá:kon?"
    sentence = "nonwén:ton sanyá:kon"
    assert make_question(sentence) == "Nonwén:ton ken sanyá:kon?"

    # Our generated sentence
    sentence2 = "yakonòn:we's ne érhar"
    assert make_question(sentence2) == "Yakonòn:we's ken ne érhar?"
