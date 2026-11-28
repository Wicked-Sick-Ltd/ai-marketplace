#!/usr/bin/env bash
#
# upgrade-agents.sh — upgrade every AI agent CLI installed on this machine, then
# make sure the Wicked Sick marketplaces and essential plugins are in place.
#
# Runs on macOS, Linux and Windows (Git Bash). Bash 3.2 compatible, no jq or
# Python. Idempotent: a CLI that is not installed is skipped, a marketplace or
# plugin that is already there is updated instead of re-added.
#
# Usage:
#   scripts/upgrade-agents.sh                 # everything installed here
#   scripts/upgrade-agents.sh claude codex    # only these agents
#   scripts/upgrade-agents.sh --dry-run       # print the commands, run nothing
#   scripts/upgrade-agents.sh --no-plugins    # upgrade the CLIs only
#
# Agents: claude codex agy copilot cursor-agent   (gemini is an alias for agy,
# Google Antigravity, which replaced the standalone Gemini CLI)
#
# The essential plugin sets match the dev profile of the vendor bootstraps
# (ai-claude-repo scripts/bootstrap.sh, ai-codex-repo scripts/bootstrap.py).
# Override with a space-separated list of plugin@marketplace:
#   WS_CLAUDE_PLUGINS, WS_CODEX_PLUGINS, WS_COPILOT_PLUGINS
# and, as bare names from ai-gemini-repo plugins.json: WS_AGY_PLUGINS
#
# pr-flow and the ai-*-repo plugins are private: they need authenticated GitHub
# access (gh auth login). A plugin that cannot be fetched is reported and the
# run carries on.
set -u

WS_CLAUDE_PLUGINS="${WS_CLAUDE_PLUGINS:-token-usage@wickedsick ponytail@wickedsick pr-flow@wickedsick session-lifecycle@wicked-sick estate-maintenance@wicked-sick}"
WS_CODEX_PLUGINS="${WS_CODEX_PLUGINS:-onboarding@wickedsick session-lifecycle@wickedsick pr-flow@wickedsick estate-maintenance@wickedsick product-lifecycle@wickedsick token-usage@wickedsick ponytail@wickedsick}"
WS_COPILOT_PLUGINS="${WS_COPILOT_PLUGINS:-token-usage@wickedsick ponytail@wickedsick pr-flow@wickedsick}"
WS_AGY_PLUGINS="${WS_AGY_PLUGINS:-onboarding session-lifecycle pr-flow estate-maintenance product-lifecycle token-usage ponytail}"

PUBLIC_MP="Wicked-Sick-Ltd/ai-marketplace"   # marketplace name: wickedsick
CLAUDE_MP="Wicked-Sick-Ltd/ai-claude-repo"   # marketplace name: wicked-sick
GEMINI_REPO="https://github.com/Wicked-Sick-Ltd/ai-gemini-repo.git"
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/ws-upgrade-agents"

DRY=0
PLUGINS=1
ONLY=""
FAILED=""

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)    DRY=1 ;;
    --no-plugins) PLUGINS=0 ;;
    -h|--help)    sed -n '3,27p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)           echo "Unknown option: $1 (try --help)" >&2; exit 2 ;;
    gemini)       ONLY="$ONLY agy" ;;
    *)            ONLY="$ONLY $1" ;;
  esac
  shift
done

have()   { command -v "$1" >/dev/null 2>&1; }
wanted() { [ -z "$ONLY" ] || case " $ONLY " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }
ver()    { "$1" --version 2>/dev/null | head -1; }

# Print a command, run it unless --dry-run, and record a failure without stopping.
run() {
  printf '    $ %s\n' "$*"
  [ "$DRY" -eq 1 ] && return 0
  "$@" </dev/null || { FAILED="$FAILED
  $*"; return 1; }
}

# upgrade <cli> <command...> — skip when the CLI is absent or not selected.
upgrade() {
  local cli="$1" before; shift
  wanted "$cli" || return 1
  if ! have "$cli"; then printf '\n==> %s: not installed, skipped\n' "$cli"; return 1; fi
  before="$(ver "$cli")"
  printf '\n==> %s (%s)\n' "$cli" "$before"
  run "$@" && [ "$DRY" -eq 0 ] && printf '    %s -> %s\n' "$before" "$(ver "$cli")"
  return 0
}

claude_plugins() {
  local installed spec id mps
  # Add by name only when missing: `add` refuses a name that is already
  # registered from another source (older machines have wicked-sick from the
  # repo's previous name, Wicked-Sick-Ltd/claude-repo).
  mps="$(claude plugin marketplace list 2>/dev/null)"
  printf '%s\n' "$mps" | grep -qE '❯ wickedsick$'  || run claude plugin marketplace add "$PUBLIC_MP"
  printf '%s\n' "$mps" | grep -qE '❯ wicked-sick$' || run claude plugin marketplace add "$CLAUDE_MP"
  run claude plugin marketplace update wickedsick
  run claude plugin marketplace update wicked-sick
  installed="$(claude plugin list --json 2>/dev/null | grep -oE '"id": *"[^"]+"' | cut -d'"' -f4)"
  # Install an essential only when no plugin of that name is installed from any
  # marketplace: the same plugin from two marketplaces loads twice.
  for spec in $WS_CLAUDE_PLUGINS; do
    printf '%s\n' "$installed" | grep -q "^${spec%@*}@" || run claude plugin install "$spec"
  done
  for id in $(printf '%s\n' "$installed" | grep -E '@(wickedsick|wicked-sick)$'); do
    run claude plugin update "$id"
  done
}

codex_plugins() {
  local installed spec id src
  # `marketplace add` refuses a marketplace that is already registered.
  codex plugin marketplace list 2>/dev/null | grep -qw wickedsick \
    || run codex plugin marketplace add "$PUBLIC_MP"
  run codex plugin marketplace upgrade
  # One "id source" line per installed plugin; source is the last column.
  installed="$(codex plugin list 2>/dev/null | awk '$2 ~ /^installed/ {print $1, $NF}')"
  for spec in $WS_CODEX_PLUGINS; do
    printf '%s\n' "$installed" | grep -q "^${spec%@*}@" || run codex plugin add "$spec"
  done
  # Codex has no `plugin update`; re-adding an installed plugin reinstalls it
  # from the refreshed marketplace snapshot.
  # Here-string, not a pipe: a piped loop would lose run()'s failure record.
  while read -r id src; do
    [ -n "$id" ] || continue
    # A marketplace added with --sparse .agents/plugins has no plugins/ tree,
    # so its in-repo plugins cannot be reinstalled from it.
    case "$src" in
      /*) [ -d "$src" ] || { printf '    skip %s: %s is missing (marketplace added with --sparse?)\n' "$id" "$src"; continue; } ;;
    esac
    run codex plugin add "$id"
  done <<<"$(printf '%s\n' "$installed" | grep -E '^[^ ]+@(wickedsick|wicked-sick-codex) ')"
}

# Untested: no Copilot CLI on the machine this was written on. The
# commands are the ones docs/ponytail.md documents.
copilot_plugins() {
  local spec
  run copilot plugin marketplace add "$PUBLIC_MP"
  for spec in $WS_COPILOT_PLUGINS; do run copilot plugin install "$spec"; done
}

# fetch_at <dir> <url> <ref> — shallow checkout of one commit or branch into a
# cache directory, reused on the next run.
fetch_at() {
  # git init only creates the leaf directory; parents (e.g. $CACHE) must exist.
  mkdir -p "$1" || return 1
  [ -d "$1/.git" ] || run git init -q "$1" || return 1
  run git -C "$1" fetch -q --depth 1 "$2" "$3" && run git -C "$1" checkout -q --detach FETCH_HEAD
}

# Antigravity installs a plugin from a local directory, not from a marketplace.
# The catalog is ai-gemini-repo plugins.json: in-repo plugins live under its
# plugins/, remote ones are a url pinned to a sha. `agy plugin install`
# replaces an existing installation, so this also updates.
agy_plugins() {
  local catalog="$CACHE/ai-gemini-repo" name src pin
  fetch_at "$catalog" "$GEMINI_REPO" main || return 0
  if [ ! -f "$catalog/plugins.json" ]; then
    printf '    (dry run: the plugin steps need the catalog, which is not cached yet)\n'
    return 0
  fi
  for name in $WS_AGY_PLUGINS; do
    src="$catalog/plugins/$name"
    if [ ! -d "$src" ]; then
      # Remote entry: print "url sha" from the lines that follow its name.
      pin="$(awk -v n="\"$name\"," '$1 == "\"name\":" { f = ($2 == n) }
        f && $1 == "\"url\":" { u = $2 } f && $1 == "\"sha\":" { print u, $2; exit }' \
        "$catalog/plugins.json" | tr -d '",')"
      if [ -z "$pin" ]; then
        FAILED="$FAILED
  agy: $name is not in ai-gemini-repo plugins.json"
        printf '    %s: not in the catalog\n' "$name"
        continue
      fi
      src="$CACHE/$name"
      # shellcheck disable=SC2086  # pin is "url sha", split on purpose
      fetch_at "$src" $pin || continue
    fi
    run agy plugin install "$src"
  done
}

upgrade claude claude update && [ "$PLUGINS" -eq 1 ] && claude_plugins
upgrade codex codex update   && [ "$PLUGINS" -eq 1 ] && codex_plugins
upgrade agy agy update       && [ "$PLUGINS" -eq 1 ] && agy_plugins
# Untested here (CLIs not installed): the copilot and cursor-agent update commands.
upgrade copilot copilot update && [ "$PLUGINS" -eq 1 ] && copilot_plugins
upgrade cursor-agent cursor-agent update

if [ -n "$FAILED" ]; then
  printf '\nFailed:%s\n' "$FAILED" >&2
  exit 1
fi
printf '\nDone. Restart running agent sessions to load the new versions.\n'
