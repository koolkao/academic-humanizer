# Testing the skill

The tests are behavioral: an agent runs the skill on a synthetic manuscript, and the output is scored
against a rubric. Re-run them after any edit to `SKILL.md` or `examples/`.

- `fixtures/`: synthetic manuscripts with deliberate traps (see `cases.md` for what each one tests).
- `cases.md`: one entry per case, with the files, the exact prompt, and MUST / MUST-NOT criteria.
- `prepare_run.sh`: copies a case's fixtures into a fresh run directory.

## Run a case

```bash
bash tests/prepare_run.sh C02 /tmp/ah-runs/C02-r1
```

Then start a fresh agent session (or subagent) with no other context:

> Read the skill at `<repo>/SKILL.md` (and `examples/before-after.md`) and follow it. The skill's
> directory is `<repo>`. Task from the author: "<prompt from cases.md, with `<run>` replaced>". Write
> files only inside the run directory. Do not ask clarifying questions.

Run each case at least twice. A single sample can pass or fail by luck. To compare against upstream,
point the same prompt at the upstream `SKILL.md` instead.

## Score a case

1. Run the token check: `python3 scripts/preservation_check.py tests/fixtures/<file> <run>/<revised>`.
2. Check that the original was not modified: `cmp tests/fixtures/<file> <run>/<file>`.
3. Read the revised file and the report against each MUST / MUST-NOT for the case and the cross-cutting
   checks. Read every flagged item yourself. Token counts alone overstate both passes and failures.
4. Record the results in `CHANGELOG.md` under the version being tested.

## Adding a case

Each new fixture should have at least one trap that a careless editor would "fix" and one that a style
rule would tempt it to remove. Write the rubric before running the case, and confirm that the upstream
skill or a no-skill run actually fails it. A case nothing ever fails isn't testing anything.
