#!/usr/bin/env bash
# Weekly status report for api-pytest (demo; intended to run Fridays 10pm).
#
# 1. Claude Code (headless, read-only + one JSON write) reviews:
#      - docs/todo/*_blueprint.txt and docs/design/*_design.txt  (the planned tasks)
#      - this week's git commits on all local branches + uncommitted changes
#    and writes docs/status/.work/<MM-DD-YYYY>.json
# 2. build_status_docx.py turns that JSON into docs/status/<MM-DD-YYYY>.docx
#    with the columns: Name of Task | Reference File | Status | Comment
#
# Usage: .claude/scheduled/weekly-status.sh            (report for today)
#        REPORT_DATE=11-20-2026 .claude/scheduled/weekly-status.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

REPORT_DATE="${REPORT_DATE:-$(date +%m-%d-%Y)}"
WEEK_START="$(date -v-6d +%Y-%m-%d)"          # macOS date; 7-day window incl. today
WEEK_END="$(date +%Y-%m-%d)"
OUT_DIR="docs/status"
JSON="$OUT_DIR/.work/$REPORT_DATE.json"
DOCX="$OUT_DIR/$REPORT_DATE.docx"
LOG="$SCRIPT_DIR/logs/weekly-status-$REPORT_DATE.log"
CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude || echo "$HOME/.local/bin/claude")}"

mkdir -p "$OUT_DIR/.work" "$SCRIPT_DIR/logs"
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date) weekly status $REPORT_DATE (week $WEEK_START..$WEEK_END) ==="

# Private Python env for python-docx, so the project's .venv/requirements stay untouched.
VENV="$SCRIPT_DIR/.venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q python-docx
fi

PROMPT=$(cat <<EOF
You are writing the weekly status report for the api-pytest project (a Python + pytest API test suite).
Report date: $REPORT_DATE. Week covered: $WEEK_START to $WEEK_END (inclusive).

Gather the facts (read-only):
1. Planned tasks: every file in docs/todo/ (*_blueprint.txt) and docs/design/ (*_design.txt).
   One task per <name>; the blueprint and design with the same <name> are the same task.
   Read each one to learn the task's goal, the files/folders it plans to create or change, and its plan steps.
2. Actual changes this week:
   - git log --branches --since="$WEEK_START 00:00" --until="$WEEK_END 23:59" --name-status --format='%h %ad %s' --date=short
   - git status --short   and   git diff --stat HEAD   (uncommitted work)
   Compare those changes with the files/folders each task says it will touch
   (e.g. tests/, helpers/, clients/, configs/, conftest.py, test_data/, README.md, .claude/).
   Open changed files when needed to judge how far the plan has progressed.

Decide a Status for each task, using exactly one of:
   Not started   - blueprint exists, no design and no related changes
   Designed      - design file exists, no related code changes yet
   In progress   - related changes exist but plan steps remain
   Done          - all plan steps appear implemented
   Blocked       - something prevents progress (say what in the comment)
Also add one row named "Other changes (no blueprint)" if this week's changes include work not covered by any task (skip it if there is none).

Comment: 1-3 short sentences of evidence - what changed this week (files, commit hashes) or why it hasn't moved, and the next step.

Write ONLY this file: $JSON  - valid JSON, exactly this shape:
{"report_date": "$REPORT_DATE", "week_start": "$WEEK_START", "week_end": "$WEEK_END",
 "tasks": [{"name": "...", "reference_files": ["docs/todo/..._blueprint.txt", "docs/design/..._design.txt"],
            "status": "...", "comment": "..."}]}
If there are no blueprints or designs, write "tasks": [] plus the "Other changes" row if applicable.
Do not modify any other file, run tests, commit, or push.
EOF
)

rm -f "$JSON"
# The Stop hook verifies code changes; this run only writes a JSON file.
SKIP_VERIFY_HOOK=1 "$CLAUDE_BIN" -p "$PROMPT" \
  --permission-mode default \
  --allowedTools "Read" "Glob" "Grep" \
    "Bash(git log *)" "Bash(git status *)" "Bash(git diff *)" "Bash(git show *)" "Bash(git branch *)" \
    "Bash(ls *)" "Edit($OUT_DIR/.work/**)"

if [ ! -s "$JSON" ]; then
  echo "ERROR: Claude did not produce $JSON" >&2
  exit 1
fi

"$VENV/bin/python" "$SCRIPT_DIR/build_status_docx.py" "$JSON" "$DOCX"
echo "Report written: $PROJECT_DIR/$DOCX"
