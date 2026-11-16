# academic-humanizer (fidelity-first fork)

An agent skill that edits AI-assisted papers and grant proposals so they read like the author wrote
them. It removes generic AI phrasing ("In recent years…", "paves the way", "delve", clause-stacked
sentences) without changing what the science says. Numbers, citations, hedges, and claims stay
exactly as written; anything substantive is proposed to you, not applied.

Fork of [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)
(v0.3.3, MIT).

## Demo (2:19)

https://github.com/user-attachments/assets/eebcb423-3e0b-4d3f-9f3f-cd5db96e756a

Every example in the video is real output from the test runs in `tests/`. If the player doesn't load,
[download the video](https://github.com/koolkao/academic-humanizer/releases/download/v0.2.0/academic-humanizer-demo.mp4)
from the v0.2.0 release.

## Use it

Paste this repo's URL into your agent (Claude Code, Codex, Cursor, or similar) and ask it to use the
skill:

```
Use the skill at https://github.com/koolkao/academic-humanizer to edit main.tex.
Target venue: a pediatrics journal.
```

That's it. The agent reads `SKILL.md` and follows it. Some optional things you can add:

- "Match my voice from prior_paper.pdf"
- "Here are numbers you may use: …" (the skill only adds numbers that are in your manuscript or that
  you supply)
- "Just audit it, don't change anything", or "Compare draft-v1.tex and draft-v2.tex"

**What you get:** your original file is left untouched. Next to it, the skill writes:
- `main.revised.tex`: the edited copy;
- `main.changes.md`: a report covering what changed, what needs your input (e.g. an inconsistent
  sample size), suggested changes it did *not* apply, and the result of a numbers-and-citations check.

## What it does differently from upstream

- **Priority order.** Fidelity comes first, then citations, then author intent and venue, then clarity,
  then style. A style rule never overrides preservation.
- **Edit vs. propose.** Prose edits are applied. Changes to claims, hedges, aims, limitations, and
  citations are only proposed, except for weakening a claim toward evidence already in the manuscript,
  which is applied but listed for the author to confirm. Apparent errors are flagged, never silently
  corrected.
- **No invented evidence.** Numbers, pointers, datasets, and citations can come only from the
  manuscript or an evidence block the user supplies. Upstream's examples that added unsupported numbers
  or cut a five-citation list to one have been replaced (`examples/before-after.md`).
- **Original kept.** The default output is `<name>.revised.<ext>` plus `<name>.changes.md`. The original
  is overwritten only on explicit request.
- **Meaning locks.** Edits must never upgrade association to causation, "suggests" to "shows", a null
  result to a "trend", planned work to completed work, "need not" to "does not", or a sample to "all".
- **Checks that actually ran.** `scripts/preservation_check.py` (standard library only) has two tiers.
  FAIL covers citations, numbers, number+unit pairs, statistics, operators, math, URLs, source comments,
  LaTeX labels/refs/environments/bibliography, and locked declarations. CHECK covers citation grouping,
  direction words, hedge, negation, modality, causal, scope, and tense wording. The report lists what was
  checked and what differed, and it never asserts "all facts preserved" without a check.
- **Modes.** edit (default), voice (match a writing sample), audit (report only), check (compare two
  versions), inline (prose only, for embedded calls).
- **Bounded access.** Only user-identified files are read. Document text is data: instructions embedded
  in a manuscript are flagged, not followed. There is no network access, credential access, or
  installation.
- **Contextual style rules.** Em-dashes, "demonstrate", and similar items are preferences, not bans.
  Quotations, theorems, and venue style win.

## Keep a copy (optional)

To use the skill without pasting the URL each time, or to pin a version you've reviewed, copy it
into your project. Claude Code picks it up as `/academic-humanizer`:

```bash
git clone https://github.com/koolkao/academic-humanizer .claude/skills/academic-humanizer
```

For confidential manuscripts, prefer a reviewed copy over a live URL, and restrict file and network
access in your agent's settings. The skill itself asks for no network access, but skill instructions
are not a sandbox.

## Tested

10 synthetic cases cover these trap types, with pass/fail rubrics in `tests/cases.md`:
- an RCT, a LaTeX ML paper, NIH Aims with an evidence block, qualitative sociology, a clinical
  abstract, a rebuttal letter, voice matching, Chicago notes;
- a detector-evasion request and an in-place request.

In 0.2.0 the fork passed 20/20 runs. Upstream v0.3.3 passed 0/7 on the same prompts (2/7 on content
alone). Upstream's failures:
- writing new hypotheses and claims directly into the manuscript;
- inventing plan details;
- overwriting originals;
- asserting checks it never ran.

Details, caveats, and known weak spots are in `CHANGELOG.md`. Method is in `docs/methods.md`.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'   # checker unit tests
bash tests/prepare_run.sh C03 /tmp/ah/C03-r1           # set up a behavioral run (see tests/README.md)
```

## Limitations

- The token check is heuristic. It can miss unusual citation formats and flag harmless reformatting.
  A clean result does not prove meaning was preserved, so the semantic review in the report still
  matters.
- This is a prose aid, not a detector-evasion tool, and it makes no claim about AI-detector outcomes.
  Follow your venue's AI-use disclosure policy.
- Validation is small: one model family, 1–2 runs per case, synthetic fixtures. See *Threats to
  validity* in `docs/methods.md`. Re-run the cases in your environment before using it with
  confidential manuscripts.

## Credits

The style catalog, proposal-mode structure, and original concept are from
[AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer). That
project builds on [blader/humanizer](https://github.com/blader/humanizer) (MIT) and
[koaeraser/ARMS](https://github.com/koaeraser/ARMS). MIT license; see `LICENSE`.
