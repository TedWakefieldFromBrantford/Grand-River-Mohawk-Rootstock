# Grand-River-Mohawk-Rootstock — Phase Handoff

## Current State: Phase 1 Complete ✅

The prefix engine is green: **218/218 forms pass**.

### Modules
- `stem_classes.py` — transitive (`PURPLE_PREFIX_MATRIX`) and intransitive (`PREFIX_MATRIX`) prefix matrices, keyed by `(subject, object)`, with stem classes C/A/I/E/O.
- `reflexive_engine.py` — `REFLEXIVE_MATRIX` and `RECIPROCAL_MATRIX` from textbook Page 47.
- `exceptions_engine.py` — documented textbook irregulars. Kept intentionally small (5 entries).
- `prefix_engine.py` — orchestrator: `_engine_key` → `_get_prefix` → `apply_phonology` → `apply_exceptions`.
- `test_prefix_engine.py` — pytest suite reading from `instance/mohawk.db`.

### Known Deferred Decisions
1. **Stem-class override SOP** — currently `conjugate(..., stem_class=None)` infers from root's first letter. Manual override exists per-call. **Decision pending**: move to global dict (Option B) or DB column (Option C).
2. **`yóhswenhs` exception** — currently overrides matrix `ka`. Verify against textbook page before next refactor.
3. **`3n` object handling** — `3n` is distinct from `3i` in the transitive matrix (needed for `3i -> 3n` = `yon-`). But it's normalized to `3i` for reflexive lookups.

## Phase 2 (Next): Stative Verb Engine

### The Template
`[Tense Pre-Prefix] + [Blue Prefix] + [Root] + [Tense Suffix]`

### Tenses (see textbook pages 205-217)
- **Present**: no pre-prefix, no suffix
- **Past**: no pre-prefix, `-kwe` or `-hne` suffix
- **Future**: `en-` or `ten-` pre-prefix, `-hake` or `-eke` suffix
- **Conditional**: `a-` or `ta-` pre-prefix, `-hake` or `-eke` suffix
- **Command**: no pre-prefix, `-k` or `-hak` suffix

### Special Cases
- **`te-` + A/C stems**: some roots take `te-` as pre-prefix even in present (`tewahwihshenhé:yon` = "I am tired").
- **`ni-` insertion**: Page 213 shows `ni-` inserted before certain C-stems, which can change the root's initial vowel.
- **Blue Prefix layer**: use `prefix_engine.conjugate()` for the Blue Prefix layer only — do not duplicate the matrix.

### First Test Verbs (Phase 2)
1. `-ahsénthos` ("cry") — `te-` pre-prefix, A-stem, Page 216
2. `-hí:ke's` ("be here") — `en-`/`a-` pre-prefixes, Page 206

### Phase 2 Kickoff Prompt

> I'm continuing the Grand-River-Mohawk-Rootstock project. Phase 1 is complete (prefix engine green, 218/218). Now starting Phase 2: Stative Verb Engine.
>
> The template is `[Tense Pre-Prefix] + [Blue Prefix] + [Root] + [Tense Suffix]`.
>
> Architecture constraint: the stative engine must *call* `prefix_engine.conjugate()` for the Blue Prefix layer, not duplicate it. New module: `stative_engine.py`.
>
> First test verbs: `-ahsénthos` (cry, te- + A-stem) and `-hí:ke's` (be here, en-/a- pre-prefixes).
>
> Start by showing me a table of expected forms for both verbs across all 5 tenses (Present, Past, Future, Conditional, Command), drawn from pages 205-217. I'll verify against the textbook before any code is written. Then propose the module layout.
>
> Attached: pages 205-217 scans, current `prefix_engine.py`, `stem_classes.py`, `reflexive_engine.py`, `exceptions_engine.py`.
