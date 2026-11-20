# transitive_engine.py

class TransitiveEngine:
    def __init__(self, verb):
        self.verb = verb

    def generate(self, aspect, subject, obj):
        from models import VocabForm
        
        # 1. Try exact match first
        vf = VocabForm.query.filter_by(
            verb_id=self.verb.id, 
            form_type=aspect, 
            subject=subject,
            object=obj
        ).first()

        # 2. Fallback to object=None (for intransitive "it" forms)
        if not vf and obj:
            vf = VocabForm.query.filter_by(
                verb_id=self.verb.id, 
                form_type=aspect, 
                subject=subject,
                object=None
            ).first()

        if not vf:
            return {"surface_form": "TODO", "trace": [], "error": f"Form not in DB for {subject} > {obj}"}
        
        sorted_trace = sorted(vf.morpheme_trace, key=lambda x: x.sequence_order)
        
        prefix, root, suffix = "", "", ""
        for trace_item in sorted_trace:
            m = trace_item.morpheme
            if m.type == "prefix": prefix = m.text.strip("-")
            elif m.type == "root": root = m.text.strip("-")
            elif m.type == "suffix": suffix = m.text.strip("-")

        # ==========================================
        # TRANSITIVE PHONOLOGY RULES
        # ==========================================
        # (None needed yet! The root already carries the accent in the DB.)
        
        # Assemble final surface form
        surface_form = prefix + root + suffix

        ui_trace = [
            {"step": "prefix", "value": prefix, "note": f"{subject} > {obj or 'it'} prefix"},
            {"step": "root", "value": root, "note": "Verb root"}
        ]

        return {"surface_form": surface_form, "trace": ui_trace}
