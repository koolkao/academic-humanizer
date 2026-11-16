# academic-humanizer (fidelity-first fork)

A fidelity-first fork of [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)
(upstream commit `94b88b23703bed7df507acae7d6d5876209a0cdf`, v0.3.3, MIT).

It is an editing pass for AI-assisted papers and grant proposals. It removes generic AI phrasing
("In recent years…", "paves the way", "delve", clause-stacked sentences) and matches the author's voice.
Factual and scientific fidelity outranks every style rule.

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

## Install (project-scoped, pinned)

Copy a reviewed version into the project that needs it instead of cloning a moving branch into a
user-wide directory:

```bash
mkdir -p .claude/skills
cp -R /path/to/this/repo .claude/skills/academic-humanizer
```

The skill declares `Read, Write, Edit, Grep, Glob, AskUserQuestion`. It does not pre-approve shell
access, so the host asks before running the preservation check. Tool declarations are not a sandbox;
enforce path and network restrictions in the host environment for confidential manuscripts.

Review upstream diffs before adopting updates. There is no automatic sync.

## Use

```
/academic-humanizer
Edit main.tex. Target venue: a pediatrics journal. Match my voice from prior_paper.pdf.
Evidence block (optional): <numbers or results the edit may use>
```

Output: `main.revised.tex`, plus `main.changes.md` with these sections: files, unresolved issues,
claim-strength changes and evidence-block additions, substantive proposals, prose edits, preservation
check.

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
