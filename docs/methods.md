# Methods: how this fork was built and tested

This document records how `academic-humanizer` (fidelity-first fork) was derived from upstream, what
evidence drove each change, and how it was validated. Results and dates are in `CHANGELOG.md`;
this file covers the method.

## 1. Starting point

- **Upstream:** [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer),
  commit `94b88b23703bed7df507acae7d6d5876209a0cdf` (v0.3.3, MIT).
- **Prior review:** [`upstream-review-and-proposal.md`](upstream-review-and-proposal.md), a manual
  static security and research-integrity review of the same commit. Its main findings:
  - low security risk;
  - examples that add unsupported evidence;
  - one example that cuts five citations to one;
  - rigid style bans;
  - broad write access with no copy-first default.

## 2. Static review (re-done for this fork)

Every upstream file was read in full: SKILL.md, examples, README, LICENSE, and the SVG assets. Each
"before → after" example in SKILL.md and `examples/before-after.md` was checked for whether every
fact in the "after" can be traced to the "before". Most cannot. The "afters" add accuracy deltas,
p-values, dataset names, table pointers, and "partner hospitals (letters enclosed)". The README's own
"after" adds "We demonstrate it on autonomous driving and network management". This confirmed the
prior review's integrity concern and found more instances of it.

## 3. Test-first development

The skill was developed in the RED → GREEN → REFACTOR cycle used for agent skills: watch an agent fail
without the change, write the change, watch it pass, close loopholes.

### 3.1 Fixtures

Synthetic manuscripts in `tests/fixtures/` each carry deliberate traps:
- something a careless editor would "fix" (a sample-size inconsistency, a dose mismatch, a wrong gap
  to the strongest baseline);
- something a style rule would tempt it to remove (an evidence-tied hedge, an em-dash inside a quote,
  "prove" applied to a theorem, first-person "I" in qualitative work);
- something that tests boundaries (an HTML or LaTeX comment addressed to "the AI assistant", a request
  to beat detectors, a request to overwrite in place).

`tests/cases.md` pairs each fixture with the author's exact prompt and MUST / MUST-NOT criteria. The
criteria were written before any run.

### 3.2 Runs

Each run is a fresh agent with no other context. It is told to read a given SKILL.md and do the task
from `cases.md`. Run directories are created by `tests/prepare_run.sh`. Runs use the same prompt for
both arms:
- **fork arm:** this repo's SKILL.md, two runs per case;
- **upstream arm:** upstream v0.3.3 SKILL.md, one or two runs per case.

### 3.3 Scoring

1. **Mechanical** (`tests/score_runs.py`):
   - original unchanged;
   - revised file present;
   - six report sections in order;
   - preservation-check exit code;
   - no `[AUTHOR]` or placeholder markers in the manuscript.
2. **Rubric:** a separate agent (not the one that produced the output) scores each run against
   `cases.md` and must quote the output line behind every failure or borderline call.
3. **Manual spot-check:** the author of this fork read every flagged item and a sample of passing
   outputs. Token counts alone overstate both passes and failures. For example, an "added number" is
   often a value correctly copied from the paper's own table.

### 3.4 Iteration history

| Version | What drove it | Change |
|---|---|---|
| 0.1.0 | Upstream baseline on fixture 01 (2 runs). Failures: a hidden comment was replaced with `[passage omitted]` (content loss); an evidence-tied hedge was dropped; an inferred claim was added; `[AUTHOR]` markers went into the prose; "no number was changed" was asserted without a check | Priority order, edit-vs-propose table, copy-first output, six-section report contract, `preservation_check.py`, repaired examples |
| 0.2.0 | Survey of 12 active upstream forks (`docs/fork-survey.md`) | FAIL/CHECK tiers; number+unit, operator, comment, LaTeX-structure, and declaration-section checks; `--protect`/`--accept`; "never upgrade" meaning locks; modes (edit/voice/audit/check/inline); more AI tells with false-positive guards; 8 fixtures and 10 cases |

## 4. The preservation checker

`scripts/preservation_check.py` uses only the standard library and reads only the two files it is
given. It makes no network access. Its design choices:
- **Multisets, not diffs.** It compares token counts so that legitimate reordering passes, but any
  added, dropped, or changed token fails.
- **Strip, then count.** Comments, citations, math, URLs, and LaTeX keys are removed before numbers
  are counted, so a citation number is never counted twice and a `\label{eq:1}` is not mistaken for
  data.
- **Unit pairing.** "500 mcg" → "500 mg" fails even though the bare number is unchanged.
- **Two tiers.** FAIL holds what must not change. CHECK holds wording that may change legitimately
  but must be reviewed: hedges, negation, modality, causal and association wording, scope, tense,
  direction, and number words. Making CHECK items fail would punish every correct
  causal→associational fix.
- **Explicit waivers.** `--accept` turns a FAIL difference into a named ACCEPTED one. The report
  must explain every waiver, and the checker prints unused waivers.
- **Honest limits.** The report ends by listing what a script cannot see.

Unit tests: `python3 -m unittest discover -s tests -p 'test_*.py'`. They cover every FAIL section,
the waiver logic, and CHECK-tier signals, and check that every fixture is clean against itself.

Known limits: it uses regex, not a TeX or Markdown parser, so unusual citation macros or Unicode
digits can be missed. Superscripts inside units (m²) can register as note markers. It cannot judge
which claim a citation supports.

## 5. Threats to validity

- **Small samples.** Two runs per case per arm, with one model family as editor and grader.
- **Synthetic fixtures.** They were written by the same agent that wrote the skill. The traps are
  real failure types, but the prose is not drawn from real manuscripts.
- **Grader correlation.** The rubric grader is the same model family as the editor. Rubrics require
  quoted evidence to limit this.
- **Harness effects.** In early runs, some host environments redacted HTML comments before the agent
  saw them. The fixture still tests the right behavior (keep the bytes, don't write a placeholder),
  but how agents perceive it varies by host.

Before using this skill on confidential manuscripts, re-run the cases in your own environment, and
add a fixture from your own field.

## 6. Reproducing

```bash
python3 -m unittest discover -s tests -p 'test_*.py'          # checker unit tests
bash tests/prepare_run.sh C02 /tmp/ah/C02-r1                   # set up a run
# ... start a fresh agent with the prompt from tests/cases.md ...
python3 tests/score_runs.py /tmp/ah                            # mechanical checks
```

Then score each run against `tests/cases.md` by reading the outputs.
