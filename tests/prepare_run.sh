#!/usr/bin/env bash
# Copy the fixtures for one test case into a fresh run directory.
#   bash tests/prepare_run.sh C03 /tmp/ah-runs/C03-r1
set -euo pipefail

case_id="${1:?usage: prepare_run.sh <case-id> <run-dir>}"
run_dir="${2:?usage: prepare_run.sh <case-id> <run-dir>}"
here="$(cd "$(dirname "$0")" && pwd)"
fx="$here/fixtures"

case "$case_id" in
  C01|C09) files=(01-pediatric-sleep.md) ;;
  C02)     files=(02-ml-paper.tex) ;;
  C03)     files=(03-nih-aims.md 03-nih-aims.evidence.md) ;;
  C04)     files=(04-qualitative-sociology.md) ;;
  C05)     files=(05-clinical-rct-abstract.md) ;;
  C06|C10) files=(06-rebuttal-letter.md) ;;
  C07)     files=(07-voice-match.draft.md 07-voice-match.sample.md) ;;
  C08)     files=(08-humanities-chicago.md) ;;
  *) echo "unknown case: $case_id" >&2; exit 2 ;;
esac

if [ -e "$run_dir" ] && [ -n "$(ls -A "$run_dir" 2>/dev/null)" ]; then
  echo "run dir not empty: $run_dir" >&2; exit 1
fi
mkdir -p "$run_dir"
for f in "${files[@]}"; do cp "$fx/$f" "$run_dir/"; done
echo "$case_id -> $run_dir: ${files[*]}"
