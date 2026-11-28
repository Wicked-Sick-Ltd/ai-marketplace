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
  # One "id scope" line per installation.
  installed="$(claude plugin list --json 2>/dev/null | tr -d '",' \
    | awk '$1 == "id:" { id = $2 } $1 == "scope:" { print id, $2 }')"
  # Install an essential only when no plugin of that name is installed from any
  # marketplace: the same plugin from two marketplaces loads twice.
  for spec in $WS_CLAUDE_PLUGINS; do
    printf '%s\n' "$installed" | grep -q "^${spec%@*}@" || run claude plugin install "$spec"
  done
  # User scope only, and named explicitly: an unscoped update picks the most
  # specific scope for the current directory, and project or local installs
  # belong to their projects, not to a machine-wide upgrade.
  for id in $(printf '%s\n' "$installed" | awk '$2 == "user" && $1 ~ /@(wickedsick|wicked-sick)$/ { print $1 }'); do
    run claude plugin update "$id" --scope user
  done
}

codex_plugins() {
  local installed spec id src tab
  tab="$(printf '\t')"
  # `marketplace add` refuses a marketplace that is already registered.
  codex plugin marketplace list 2>/dev/null | grep -qw wickedsick \
    || run codex plugin marketplace add "$PUBLIC_MP"
  run codex plugin marketplace upgrade
  # One "id<TAB>local source path" line per installed plugin, from the JSON
  # listing so a path with spaces or a Windows drive letter survives. The path
  # is empty for a plugin fetched from Git (a git-subdir source also has a
  # "path", relative to its repository, which is not a local directory).
  installed="$(codex plugin list --json 2>/dev/null | awk '
    function val(s) { sub(/^[^:]*: *"/, "", s); sub(/",?[ \r]*$/, "", s); gsub(/\\\\/, "\\", s); return s }
    function flush() { if (id != "") print id "\t" path; id = ""; path = ""; loc = 0 }
    /^  "available"/      { exit }
    /"pluginId":/         { flush(); id = val($0) }
    /"source": *"local"/  { loc = 1 }
    /"path":/ && loc && path == "" { path = val($0) }
    END                   { flush() }')"
  for spec in $WS_CODEX_PLUGINS; do
    printf '%s\n' "$installed" | grep -q "^${spec%@*}@" || run codex plugin add "$spec"
  done
  # Codex has no `plugin update`; re-adding an installed plugin reinstalls it
  # from the refreshed marketplace snapshot.
  # Here-string, not a pipe: a piped loop would lose run()'s failure record.
  while IFS="$tab" read -r id src; do
    case "$id" in *@wickedsick|*@wicked-sick-codex) ;; *) continue ;; esac
    # A marketplace added with --sparse .agents/plugins has no plugins/ tree,
    # so its in-repo plugins cannot be reinstalled from it.
    if [ -n "$src" ] && [ ! -d "$src" ]; then
      printf '    skip %s: %s is missing (marketplace added with --sparse?)\n' "$id" "$src"
      continue
    fi
    run codex plugin add "$id"
  done <<<"$installed"
}

# Untested: no Copilot CLI on the machine this was written on. The commands and
# the `plugin list --json` row shape ({ name, marketplace?, ... }) are from
# GitHub's Copilot CLI plugin reference.
copilot_plugins() {
  local installed spec name
  copilot plugin marketplace list 2>/dev/null | grep -qw wickedsick \
    || run copilot plugin marketplace add "$PUBLIC_MP"
  run copilot plugin marketplace update wickedsick
  # One JSON object per line, whatever the original layout, then the names of
  # the plugins installed from this marketplace.
  installed="$(copilot plugin list --json 2>/dev/null | tr -d '\n' | tr '}' '\n')"
  for spec in $WS_COPILOT_PLUGINS; do
    printf '%s\n' "$installed" | grep -qE "\"name\": *\"${spec%@*}\"" || run copilot plugin install "$spec"
  done
  for name in $(printf '%s\n' "$installed" | grep -E '"marketplace": *"wickedsick"' \
      | grep -oE '"name": *"[^"]+"' | cut -d'"' -f4); do
    run copilot plugin update "$name"
  done
}

# fetch_at <dir> <url> <ref> — shallow checkout of one commit or branch into a
# cache directory, reused on the next run.
fetch_at() {
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
# Untested here (CLI not installed): the copilot update command.
upgrade copilot copilot update && [ "$PLUGINS" -eq 1 ] && copilot_plugins
# Cursor CLI is the one agent this script installs when missing. Its installer
# supports macOS and Linux only, so on Windows a missing CLI stays skipped.
if wanted cursor-agent && ! have cursor-agent; then
  case "$(uname -s)" in
    Darwin*|Linux*)
      printf '\n==> cursor-agent: not installed, installing\n'
      run bash -c 'curl https://cursor.com/install -fsS | bash'
      # The installer links into ~/.local/bin, which may not be on PATH yet.
      have cursor-agent || PATH="$HOME/.local/bin:$PATH" ;;
  esac
fi
upgrade cursor-agent cursor-agent update

if [ -n "$FAILED" ]; then
  printf '\nFailed:%s\n' "$FAILED" >&2
  exit 1
fi
printf '\nDone. Restart running agent sessions to load the new versions.\n'
