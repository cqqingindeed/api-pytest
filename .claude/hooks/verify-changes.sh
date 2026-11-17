#!/usr/bin/env bash
# Stop hook: verify every uncommitted change before Claude closes the task.
#   1. Every changed/new .py file must compile.
#   2. Every changed/new test file must be collectable by pytest.
#   3. If the API under test is reachable, the changed tests must pass.
# On failure it blocks the stop and hands the errors back to Claude to fix.

input=$(cat)
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

# Headless report jobs (e.g. .claude/scheduled/weekly-status.sh) change no code.
[ "${SKIP_VERIFY_HOOK:-}" = "1" ] && exit 0

# Already blocked once this turn: don't loop forever.
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi

PY=".venv/bin/python"
[ -x "$PY" ] || PY="python3"
BASE_URL="${BASE_URL:-http://localhost:3050}"

# Uncommitted changes as "STATUS<TAB>path": tracked vs HEAD plus untracked (not ignored).
all_changes=$( { git diff --name-status --no-renames HEAD 2>/dev/null;
                 git ls-files --others --exclude-standard 2>/dev/null | sed 's/^/A	/'; } | sort -u -k2 )
[ -z "$all_changes" ] && exit 0
# Files that still exist (deleted files are summarised but not verified).
changed=$(echo "$all_changes" | cut -f2- | while read -r f; do [ -f "$f" ] && echo "$f"; done)

# names of def/class in a stream of lines, comma-separated
names() { grep -oE '(def|class)[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' | awk '{print $2}' | awk '!s[$0]++' | paste -sd, - | sed 's/,/, /g'; }

# One line per file: path, status, line counts, and which defs/classes changed.
summarize() {
  echo "$all_changes" | while IFS=$'\t' read -r st f; do
    [ -z "$f" ] && continue
    if [ "$st" = "D" ]; then
      echo "- $f — deleted"
      continue
    fi
    if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
      diff=$(git diff -U0 HEAD -- "$f")
      add=$(echo "$diff" | grep -cE '^\+[^+]|^\+$')
      del=$(echo "$diff" | grep -cE '^-[^-]|^-$')
      line="- $f — modified (+$add/-$del lines)"
      if [[ "$f" == *.py ]]; then
        added=$(echo "$diff" | grep -E '^\+[[:space:]]*(async[[:space:]]+)?(def|class)[[:space:]]' | names)
        removed=$(echo "$diff" | grep -E '^-[[:space:]]*(async[[:space:]]+)?(def|class)[[:space:]]' | names)
        touched=$(echo "$diff" | grep '^@@' | sed -E 's/^@@[^@]*@@ ?//' | names)
        # "changed" = enclosing defs of edited hunks that weren't added/removed outright
        changed_defs=$(echo "$touched" | tr ',' '\n' | sed 's/^ //' | grep -v '^$' \
          | grep -vxF -f <(echo "$added, $removed" | tr ',' '\n' | sed 's/^ //' | grep -v '^$') 2>/dev/null \
          | paste -sd, - | sed 's/,/, /g')
        [ -n "$added" ] && line="$line; added: $added"
        [ -n "$removed" ] && line="$line; removed: $removed"
        [ -n "$changed_defs" ] && line="$line; changed: $changed_defs"
      fi
    else
      n=$(wc -l < "$f" | tr -d ' ')
      line="- $f — new file ($n lines)"
      if [[ "$f" == *.py ]]; then
        defs=$(names < "$f")
        [ -n "$defs" ] && line="$line; defines: $defs"
      fi
    fi
    echo "$line"
  done
}
summary=$(summarize)

py_files=$(echo "$changed" | grep -E '\.py$')
test_files=$(echo "$py_files" | grep -E '(^|/)test_[^/]*\.py$|_test\.py$')
# conftest/helpers/clients/configs changes affect every test.
shared_changed=$(echo "$py_files" | grep -E '^(conftest\.py|helpers/|clients/|configs/)')
api_up=false
curl -s -o /dev/null --max-time 3 "$BASE_URL" && api_up=true

errors=""
add_err() { errors="${errors}$1"$'\n'; }

# 1. Syntax check
for f in $py_files; do
  out=$("$PY" -m py_compile "$f" 2>&1) || add_err "Syntax error in $f:"$'\n'"$out"
done

# 2. Collection check (imports, fixtures, markers)
# Some test modules log in at import time, so collecting the whole suite only
# works while the API is up; otherwise collect just the changed test files.
collect_note=""
if [ -n "$shared_changed" ] && $api_up; then
  collect_target="tests"
else
  collect_target="$test_files"
  [ -n "$shared_changed" ] && collect_note=" (full-suite collection skipped: API down)"
fi
if [ -n "$collect_target" ]; then
  # shellcheck disable=SC2086
  out=$("$PY" -m pytest --collect-only -q -p no:cacheprovider $collect_target 2>&1)
  rc=$?
  # rc 5 = no tests collected, which is fine
  if [ $rc -ne 0 ] && [ $rc -ne 5 ]; then
    add_err "pytest collection failed:"$'\n'"$(echo "$out" | tail -40)"
  fi
fi

# 3. Run changed tests when the API is up
ran="skipped (API at $BASE_URL not reachable)"
if [ -z "$errors" ] && [ -n "$test_files" ] && $api_up; then
  # shellcheck disable=SC2086
  out=$("$PY" -m pytest -q -p no:cacheprovider -o log_cli=false $test_files 2>&1)
  if [ $? -ne 0 ]; then
    add_err "Changed tests failed:"$'\n'"$(echo "$out" | tail -60)"
  else
    ran="passed"
  fi
fi

if [ -n "$errors" ]; then
  reason="Verification failed for uncommitted changes. Fix these before finishing:"$'\n'"$errors"$'\n'"Changed files:"$'\n'"$summary"
  jq -n --arg r "$reason" '{decision: "block", reason: $r}'
  exit 0
fi

n=$(echo "$all_changes" | wc -l | tr -d ' ')
msg="Verified $n changed file(s): syntax OK, collection OK$collect_note, tests $ran."$'\n'"Summary of changes:"$'\n'"$summary"
jq -n --arg m "$msg" '{systemMessage: $m}'
exit 0
