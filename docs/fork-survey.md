# Survey of upstream forks (2026-11-16)

Upstream had 408 forks. Stars don't separate them (the most-starred has 2), so the survey covered
the forks with commits ahead of upstream `main`, 12 in all. Their files were read as untrusted data
through the GitHub API, and none of their code was run. None makes network calls or touches
credentials.

## Adopted in 0.2.0

| Idea | Source fork | Where it landed |
|---|---|---|
| Number+unit pairing, operator counts, number words, up/down direction stems, a review tier, `--protect` / `--accept` flags that must be named in the report, and a "what the script cannot see" reread | musiddiqui85/academic-humanizer (`scripts/check_integrity.py`) | `scripts/preservation_check.py` FAIL/CHECK tiers; SKILL.md *Preservation check* |
| LaTeX invariants: labels, refs, cite keys, environments, includes, macros, the bibliography block; locked AI-use / data-availability / CRediT declarations | hongyi-zhao/academic-humanizer (`scripts/check_latex_invariants.py`, `references/latex-preservation-contract.md`) | checker LaTeX sections and locked declaration sections |
| Modality and condition direction ("need not", "only where"), planned vs. completed work, transitions that need antecedents, "never upgrade" pairs, a theorem with its assumptions | hosseinoliabak/academic-humanizer, hongyi-zhao/academic-humanizer | SKILL.md *Never upgrade (meaning locks)* |
| Invocation modes: audit only, conservative rewrite, voice-matched, invariant check, and prose-only return for embedded calls | user941go/academic-humanizer-adv | SKILL.md *Modes* |
| Phantom alternatives, drafting narration, generic endings; citation lists flagged with an author query; a false-positive guard for field terms | user941go/academic-humanizer-adv | SKILL.md *Academic tells* |

## Considered, not adopted (yet)

- **Manuscript-visibility leak check** (hongyi-zhao): flags workflow artifacts in visible text (repo
  paths, hashes, "manifest", "gate"). Useful for agent-assisted manuscripts. Candidate for 0.3.
- **Reporting-guideline audit** (chenjinfengdoctor-bit): flag-only CONSORT/STROBE/STARD/TRIPOD/ARRIVE
  checklist. Candidate as an optional domain layer.
- **Domain-distinction locks in an author profile** (keyu-wan), e.g. geographic vs. random holdout.
- **DOCX/PDF structural-count comparison** (jingyanjiang). Tied to Codex document skills.
- **"Find the argument before editing sentences"** framing pass (zzg021).

## Integrity concerns found

- **cHaoB05:** its only change deletes "not designed to evade AI-use detection" and the disclosure
  obligation.
- **musiddiqui85:** its "statistical profile" layer matches sentence-length spread and connective
  rates to a pre-2022 baseline. That is burstiness rewriting, the standard detector-evasion technique.
  Its checker was adopted; this layer was not.
- **chenjinfengdoctor-bit:** its repaired examples invent trial results ("PFS from 32% to 51% (HR
  0.58…)").
- **zzg021:** cuts the claim-evidence layer and the disclosure line, and says to "check fidelity
  quietly".
- **hosseinoliabak:** the workflow is organized around AI-detector feedback labels. It handles them
  with caveats, but the framing was not adopted.

## Cosmetic or packaging only

- ryanfan394-del: Claude plugin manifest.
- MizaR108: upstream SKILL.md moved under `skills/`.
- agityaviandra: Indonesian variant.
