# active_engine.py

class ActiveEngine:
    def __init__(self, verb, stem_class):
        self.verb = verb
        self.root = verb.root
        self.stem_class = stem_class

    def generate(self, aspect, subject):
        """
        Generic assembler: fetches the morphological trace from the DB,
        assembles the parts, and applies phonological rules.
        """
        from models import VocabForm
        
        # 1. Fetch the Gold Standard trace from the DB
        vf = VocabForm.query.filter_by(
            verb_id=self.verb.id, 
            form_type=aspect, 
            subject=subject
        ).first()

        if not vf:
            return {"surface_form": "TODO", "trace": [], "error": "Form not in DB"}
            
        if not vf.morpheme_trace:
            return {"surface_form": vf.form, "trace": [], "note": "Direct DB lookup"}

        # 2. Extract the ordered morphemes and strip hyphens
        sorted_trace = sorted(vf.morpheme_trace, key=lambda x: x.sequence_order)
        
        prefix, root, suffix = "", "", ""
        for trace_item in sorted_trace:
            m = trace_item.morpheme
            if m.type == "prefix":
                prefix = m.text.strip("-")
            elif m.type == "root":
                root = m.text.strip("-")
            elif m.type == "suffix":
                suffix = m.text.strip("-")

        # 3. Route to the correct phonological rule set
        if self.root == "-yo'ten":
            surface_form, prefix, root, suffix = self._phonology_yo_ten(prefix, root, suffix, aspect, subject)
        elif self.stem_class == "C":
            surface_form, prefix, root, suffix = self._phonology_c_stem(prefix, root, suffix, aspect, subject)
        elif self.stem_class == "A":
            surface_form, prefix, root, suffix = self._phonology_a_stem(prefix, root, suffix, aspect, subject)
        elif self.stem_class == "I":
            surface_form, prefix, root, suffix = self._phonology_i_stem(prefix, root, suffix, aspect, subject)
        else:
            surface_form = prefix + root + suffix

        # 4. Build the trace for the UI
        ui_trace = [
            {"step": "prefix", "value": prefix, "note": f"{subject} {aspect} prefix"},
            {"step": "root", "value": root, "note": "Verb root"},
            {"step": "suffix", "value": suffix, "note": f"{aspect} suffix"}
        ]

        return {"surface_form": surface_form, "trace": ui_trace}

    # ==========================================
    # C-STEM RULES (-khonn-)
    # ==========================================
    def _phonology_c_stem(self, prefix, root, suffix, aspect, subject):
        # Rule 1: Root vowel length and accent
        if root == "khonn":
            if aspect in ["habitual", "perfective"]:
                root = "khón:n"
            else:
                root = "khon"
                if not any(char in prefix for char in "áéíóú"):
                    root = "khón"

        # Rule 2: Epenthetic 'e' (k + kh -> kekh)
        if prefix == "k" and root.startswith("kh"):
            prefix = "ke"

        # Rule 3: Suffix adjustment for Definite/Indefinite/Future
        if suffix == "i'" and root.endswith("n"):
            suffix = ":ni'"
            # Degemination: khón:n + :ni' -> khón:ni'
            if root.endswith(":n"):
                suffix = "i'" # Root already has the length, so we just need 'i\''

        # Rule 4: Degemination for Perfective (khón:n + i -> khón:ni)
        if root.endswith(":n") and suffix.startswith("n"):
            suffix = suffix[1:]

        return prefix + root + suffix, prefix, root, suffix

    # ==========================================
    # A-STEM RULES (-atketskw)
    # ==========================================
    def _phonology_a_stem(self, prefix, root, suffix, aspect, subject):
        # Rule 1: Accent the 'e' in the root
        if "e" in root:
            root = root.replace("e", "é")
            
        # Rule 2: The movable 'a'
        # The root is "atkétskw". We strip the 'a' to get the base "tkétskw".
        if root.startswith("a"):
            root = root[1:]

        # Rule 3: Resurface the 'a' for specific subjects
        if subject in ["1sg", "2sg", "1pl.ex", "2pl"]:
            root = "a" + root
            
            # Rule 3a: Vowel Degemination (drop double vowels like 'a' + 'a')
            if prefix and prefix[-1] == root[0] and prefix[-1] in "aeiou":
                root = root[1:]

        # Rule 4: Consonant Degemination (drop double 't')
        if prefix.endswith("t") and root.startswith("t"):
            root = root[1:]

        return prefix + root + suffix, prefix, root, suffix

    # ==========================================
    # -yo'ten RULES (Irregular)
    # ==========================================
    def _phonology_yo_ten(self, prefix, root, suffix, aspect, subject):
        # Overrides for vowel drop
        overrides = {
            ("habitual", "3m/i"): "róy'tens",
            ("habitual", "3f"): "yakoyó'tens", 
            ("perfective", "3m/i"): "royó'tén:on", 
        }
        if (aspect, subject) in overrides:
            return overrides[(aspect, subject)], prefix, root, suffix
        
        # Accent rule for the stem
        if aspect == "habitual":
            root = "ó'ten"
        elif aspect == "perfective":
            root = "o'tén"

        return prefix + root + suffix, prefix, root, suffix

    # ==========================================
    # I-STEM RULES (-ita)
    # ==========================================

    def _phonology_i_stem(self, prefix, root, suffix, aspect, subject):
        # The DB now holds exact chunks (e.g., "wakí:" + "tah" + "s")
        # The only rule we need is to drop the 'i' from the root for perfective
        # if the prefix already ends in a consonant.

        # 1. Degemination: If prefix ends in 'n' and root starts with 't', fine.
        # No action needed, "sén:" + "tah" = "sén:tah"

        # 2. The perfective root is "tá:'on". The prefix is "waki".
        # "waki" + "tá:'on" = "wakitá:'on". Perfect.

        # 3. The 2sg perfective: "sen" + "tá:'on" = "sentá:'on". Perfect.

        # The chunks are already correct. Just assemble.
        return prefix + root + suffix, prefix, root, suffix
