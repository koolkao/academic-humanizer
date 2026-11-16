#!/usr/bin/env python3
"""Mechanical cross-cutting checks for a directory of test runs.

    python3 tests/score_runs.py RUNS_DIR

RUNS_DIR holds one subdirectory per run, named <CASE>-<tag> (e.g. C02-r1, C02-up), each created
by tests/prepare_run.sh and then edited by an agent. For each run this prints:

  orig   original fixture byte-identical (C10: expected to be overwritten)
  rev    a revised file was found
  report change report found, and whether the six contract sections appear in order
  check  preservation_check.py exit code on (fixture, revised) - 0 means no FAIL-tier differences
  marks  [AUTHOR ...] or "[passage omitted]"-style placeholders inside the revised manuscript

These are only the mechanical checks. The MUST / MUST-NOT rubric in tests/cases.md still has to be
scored by reading each output.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
CHECK = ROOT / "scripts" / "preservation_check.py"
PRIMARY = {"C01": "01-pediatric-sleep.md", "C09": "01-pediatric-sleep.md", "C02": "02-ml-paper.tex",
           "C03": "03-nih-aims.md", "C04": "04-qualitative-sociology.md",
           "C05": "05-clinical-rct-abstract.md", "C06": "06-rebuttal-letter.md",
           "C10": "06-rebuttal-letter.md", "C07": "07-voice-match.draft.md",
           "C08": "08-humanities-chicago.md"}
SECTIONS = ["files", "unresolved", "claim-strength", "substantive", "prose", "preservation"]
MARK = re.compile(r"\[AUTHOR|\[passage omitted|\[omitted|\[redacted", re.I)


def find_revised(run: pathlib.Path, primary: str, case: str) -> pathlib.Path | None:
    stem, ext = primary.rsplit(".", 1)
    if case == "C10":
        return run / primary
    cands = [p for p in run.iterdir() if p.is_file() and p.name != primary
             and p.suffix == "." + ext and stem.split(".")[0] in p.name
             and not re.search(r"change|report|evidence|sample|original|backup", p.name, re.I)]
    if not cands and (run / primary).read_bytes() != (FIX / primary).read_bytes():
        return run / primary  # edited in place
    return sorted(cands)[0] if cands else None


def find_report(run: pathlib.Path) -> pathlib.Path | None:
    cands = [p for p in run.iterdir() if re.search(r"change|report", p.name, re.I)]
    return sorted(cands)[0] if cands else None


def main() -> int:
    runs = pathlib.Path(sys.argv[1])
    print(f"{'run':10} {'orig':6} {'rev':4} {'report':14} {'check':6} marks")
    for run in sorted(p for p in runs.iterdir() if p.is_dir()):
        case = run.name.split("-")[0]
        primary = PRIMARY.get(case)
        if not primary:
            continue
        same = (run / primary).read_bytes() == (FIX / primary).read_bytes()
        orig = ("ok" if not same else "KEPT!") if case == "C10" else ("ok" if same else "CHANGED")
        rev = find_revised(run, primary, case)
        rep = find_report(run)
        if rep:
            heads = [h.lower() for h in re.findall(r"(?m)^#+\s*(?:\d+\.\s*)?(.+)$", rep.read_text())]
            pos = [next((i for i, h in enumerate(heads) if s in h), -1) for s in SECTIONS]
            rstat = "6/6 ordered" if all(p >= 0 for p in pos) and pos == sorted(pos) else \
                f"{sum(p >= 0 for p in pos)}/6"
        else:
            rstat = "none"
        code, marks = "-", "-"
        if rev and rev.exists():
            code = str(subprocess.run([sys.executable, "-I", str(CHECK), str(FIX / primary), str(rev)],
                                      capture_output=True).returncode)
            marks = str(len(MARK.findall(rev.read_text(encoding="utf-8")))) or "0"
        print(f"{run.name:10} {orig:6} {'yes' if rev else 'NO':4} {rstat:14} {code:6} {marks}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
