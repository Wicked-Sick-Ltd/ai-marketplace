#!/usr/bin/env bash
# HELP-START
# pr-wait.sh — wait until every check run and reviewer bot on a pull request has
# finished, then print a triage digest (checks, reviews, unresolved review
# threads, comments) that an agent can act on line by line.
#
# Why a script: on our repos every reviewer bot (Cursor Bugbot, Claude Code
# Review, Copilot, CodeQL, Semgrep, the test workflows) registers a check run on
# the head commit and posts its review the moment that run completes. So "all
# check runs terminal" is the one predicate that means both CI and the bots
# are done — polling `gh pr checks` alone misses reviews that land late.
# Commit statuses (the older status API) are waited on and counted with the
# check runs.
#
# Each poll is one GraphQL query for check runs, commit statuses, review
# threads and mergeability, and it also carries the reviews and issue comments
# the digest prints. That replaces the old per-poll REST calls. Before every
# poll the script reads the GraphQL rateLimit (a one-point probe on the first
# poll, then the rateLimit object on the previous response). When fewer than
# 500 points remain it sleeps until resetAt and logs that, so a shared
# 5,000/hour token is not drained.
#
# Usage:
#   pr-wait.sh [PR-number | branch | URL] [--repo OWNER/NAME] [--timeout SECS]
#              [--interval SECS] [--grace SECS] [--settle SECS] [--no-wait]
#              [--dry-run]
#   Defaults: current branch's PR, current repo, timeout 3600, interval 90,
#   grace 120 (how long to wait for the first check run to register), settle 90
#   (how long the set of completed runs must stay unchanged before we believe
#   nothing else — a reviewer bot, a `needs:` job — is still about to register).
#   A new head commit restarts the wait. PR_WAIT_RETRY_SLEEP (default 5)
#   spaces the retries of a failing gh call. PR_WAIT_INTERVAL sets the poll
#   interval when --interval is omitted (default 90). The interval must be at
#   least 60 seconds; a smaller value is a usage error.
#   --dry-run prints the effective settings and does not call GitHub.
# Exit codes:
#   0 every check passed/neutral/skipped   1 a check failed, was cancelled or timed out
#   2 gave up waiting (timeout)            3 usage, or gh kept failing (never reported as green)
# Needs: gh (authenticated), jq. Plain bash, no other deps. --dry-run needs neither.
# HELP-END
set -uo pipefail

# Fewer than this many GraphQL points remaining → sleep until the window resets.
RATE_FLOOR=500
MIN_INTERVAL=60

PR=""
REPO=""
REPO_EXPLICIT=0
TIMEOUT=3600
INTERVAL="${PR_WAIT_INTERVAL:-90}"
GRACE=120
SETTLE=90
NOWAIT=0
DRYRUN=0
RETRY_SLEEP="${PR_WAIT_RETRY_SLEEP:-5}"
LAST_REMAINING=""
LAST_RESET=""

usage() {
  awk '
    /^# HELP-START$/ { show = 1; next }
    /^# HELP-END$/ { exit }
    show { sub(/^# ?/, ""); print }
  ' "$0"
}

die() { echo "pr-wait: $*" >&2; exit 3; }

while [ $# -gt 0 ]; do
  case "$1" in
    --repo)
      [ $# -ge 2 ] || die "--repo needs a value"
      REPO="$2"; REPO_EXPLICIT=1; shift 2;;
    --timeout)
      [ $# -ge 2 ] || die "--timeout needs a value"
      TIMEOUT="$2"; shift 2;;
    --interval)
      [ $# -ge 2 ] || die "--interval needs a value"
      INTERVAL="$2"; shift 2;;
    --grace)
      [ $# -ge 2 ] || die "--grace needs a value"
      GRACE="$2"; shift 2;;
    --settle)
      [ $# -ge 2 ] || die "--settle needs a value"
      SETTLE="$2"; shift 2;;
    --no-wait) NOWAIT=1; shift;;
    --dry-run) DRYRUN=1; shift;;
    -h|--help) usage; exit 0;;
    --*) echo "pr-wait: unknown option $1" >&2; exit 3;;
    *) PR="$1"; shift;;
  esac
done

case "$INTERVAL" in
  ''|*[!0-9]*) die "interval must be a whole number of seconds (got '${INTERVAL}')";;
esac
if [ "$((10#$INTERVAL))" -lt "$MIN_INTERVAL" ]; then
  die "interval ${INTERVAL}s is below the minimum of ${MIN_INTERVAL}s"
fi

if [ "$DRYRUN" -eq 1 ]; then
  printf 'pr-wait: dry-run interval=%s timeout=%s grace=%s settle=%s rate_floor=%s min_interval=%s repo=%s pr=%s\n' \
    "$INTERVAL" "$TIMEOUT" "$GRACE" "$SETTLE" "$RATE_FLOOR" "$MIN_INTERVAL" \
    "${REPO:-(unset)}" "${PR:-(current branch)}"
  echo "pr-wait: dry-run poll=graphql checks+statuses+reviewThreads+mergeability"
  exit 0
fi

command -v gh >/dev/null || die "gh not found"
command -v jq >/dev/null || die "jq not found"

# gh_try LABEL gh-args... — up to 3 attempts; prints stdout of the first success.
# A persistent failure is fatal (exit 3): a rate limit or 502 must never be
# read back as "no checks", "no threads" or "no comments".
gh_try() {
  local label="$1"
  shift
  local attempt=1 out err cmd="$1"
  err="$(mktemp)" || die "mktemp failed"
  while [ "$attempt" -le 3 ]; do
    if out="$(gh "$@" 2>"$err")"; then
      rm -f "$err"
      printf '%s' "$out"
      return 0
    fi
    if [ "$attempt" -lt 3 ]; then
      sleep "$RETRY_SLEEP"
    fi
    attempt=$((attempt + 1))
  done
  local msg
  msg="$(tr '\n' ' ' <"$err" 2>/dev/null || true)"
  rm -f "$err"
  die "$label failed 3 times (gh ${cmd} ...): ${msg}"
}

# One combined poll. Reserved cost is nodes/100 (minimum 1): 100 contexts,
# 100 reviews, 100 threads × 20 comments, 100 issue comments. Do not add
# another nested connection without rechecking that cost.
POLL_QUERY=$(cat <<'EOF'
query($owner:String!, $name:String!, $number:Int!) {
  rateLimit { remaining resetAt cost }
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      number
      url
      state
      mergeable
      mergeStateStatus
      headRefOid
      headRefName
      baseRefName
      commits(last:1) {
        nodes {
          commit {
            oid
            statusCheckRollup {
              contexts(first:100) {
                pageInfo { hasNextPage }
                nodes {
                  __typename
                  ... on CheckRun {
                    databaseId
                    name
                    status
                    conclusion
                    title
                  }
                  ... on StatusContext {
                    context
                    state
                    description
                  }
                }
              }
            }
          }
        }
      }
      reviews(first:100) {
        pageInfo { hasNextPage }
        nodes { submittedAt state body author { login } }
      }
      reviewThreads(first:100) {
        pageInfo { hasNextPage }
        nodes {
          isResolved
          isOutdated
          path
          line
          comments(first:20) {
            nodes { author { login } body }
          }
        }
      }
      comments(first:100) {
        pageInfo { hasNextPage }
        nodes { createdAt body author { login } }
      }
    }
  }
}
EOF
)

PARSE_JQ=$(cat <<'EOF'
def lc: ascii_downcase;
.data as $root
| $root.repository.pullRequest as $pr
| ($pr.commits.nodes[0].commit // null) as $commit
| ($commit.statusCheckRollup.contexts // null) as $contexts
| {
    number: $pr.number,
    url: $pr.url,
    state: $pr.state,
    base: $pr.baseRefName,
    sha: $pr.headRefOid,
    commit: ($commit.oid // null),
    mergeable: ($pr.mergeable // "UNKNOWN"),
    merge_state: ($pr.mergeStateStatus // "UNKNOWN"),
    remaining: $root.rateLimit.remaining,
    resetAt: $root.rateLimit.resetAt,
    checks_more: ($contexts.pageInfo.hasNextPage // false),
    threads_more: ($pr.reviewThreads.pageInfo.hasNextPage // false),
    reviews_more: ($pr.reviews.pageInfo.hasNextPage // false),
    comments_more: ($pr.comments.pageInfo.hasNextPage // false),
    checks: (
      ($contexts.nodes // [])
      | map(
          if .__typename == "CheckRun" then {
            id: (.databaseId // .name),
            name: (.name // "check"),
            status: ((.status // "PENDING") | lc),
            conclusion: (if .conclusion == null then null else (.conclusion | lc) end),
            output: {title: (.title // "")}
          }
          elif .__typename == "StatusContext" then {
            id: ("status:" + (.context // "status")),
            name: (.context // "status"),
            status: (if (.state == "PENDING" or .state == "EXPECTED") then "pending" else "completed" end),
            conclusion: (
              if .state == "SUCCESS" then "success"
              elif (.state == "FAILURE" or .state == "ERROR") then "failure"
              else null end
            ),
            output: {title: (.description // "")}
          }
          else empty end
        )
    ),
    reviews: [
      $pr.reviews.nodes[]?
      | {
          submitted_at: .submittedAt,
          state: .state,
          body: (.body // ""),
          user: {login: (.author.login // "unknown")}
        }
    ],
    threads: [
      $pr.reviewThreads.nodes[]?
      | .comments = {
          nodes: [
            .comments.nodes[]?
            | {body: (.body // ""), author: {login: (.author.login // "unknown")}}
          ]
        }
    ],
    comments: [
      $pr.comments.nodes[]?
      | {
          created_at: .createdAt,
          body: (.body // ""),
          user: {login: (.author.login // "unknown")}
        }
    ]
  }
EOF
)

now() { date +%s; }

# resetAt is UTC ISO-8601 (2026-10-30T09:34:10Z). jq parses that on macOS and
# Linux. Do not shell out to date for this value: the GNU and BSD flags differ.
epoch_of() {
  local raw="$1" trimmed epoch
  if ! epoch="$(jq -nr --arg t "$raw" '$t | fromdateiso8601' 2>/dev/null)"; then
    epoch=""
  fi
  if [ -z "$epoch" ]; then
    trimmed="${raw%%.*}"
    case "$trimmed" in
      *Z) ;;
      *) trimmed="${trimmed}Z" ;;
    esac
    if ! epoch="$(jq -nr --arg t "$trimmed" '$t | fromdateiso8601' 2>/dev/null)"; then
      epoch=""
    fi
  fi
  if [ -z "$epoch" ]; then
    return 1
  fi
  printf '%s' "$epoch"
}

note_rate_limit() {
  local remaining="$1" reset="$2"
  case "$remaining" in
    ''|*[!0-9]*) die "rate limit response missing remaining";;
  esac
  if [ -z "$reset" ] || [ "$reset" = null ]; then
    die "rate limit response missing resetAt"
  fi
  LAST_REMAINING="$remaining"
  LAST_RESET="$reset"
}

read_rate_limit() {
  local raw
  raw="$(gh_try "rate limit" api graphql -f query='query { rateLimit { remaining resetAt } }')"
  if jq -e '(.errors // []) | length > 0' >/dev/null <<<"$raw"; then
    die "rate limit query failed: $(jq -r '[(.errors // [])[].message] | join("; ")' <<<"$raw")"
  fi
  note_rate_limit \
    "$(jq -r '.data.rateLimit.remaining // empty' <<<"$raw")" \
    "$(jq -r '.data.rateLimit.resetAt // empty' <<<"$raw")"
}

# Sleep out a near-empty GraphQL budget. The nap does not count toward --timeout
# or --grace: start is moved forward by the same number of seconds.
guard_rate_limit() {
  local now_s reset_epoch wait_for
  if [ -z "$LAST_REMAINING" ]; then
    read_rate_limit
  fi
  if [ "$LAST_REMAINING" -ge "$RATE_FLOOR" ]; then
    return 0
  fi
  now_s=$(now)
  reset_epoch="$(epoch_of "$LAST_RESET")" || die "could not parse rate limit reset ${LAST_RESET}"
  # Two spare seconds so we don't wake in the last tick of the old window.
  wait_for=$((reset_epoch - now_s + 2))
  if [ "$wait_for" -lt 1 ]; then
    echo "pr-wait: graphql rate limit low (${LAST_REMAINING} points remaining, floor ${RATE_FLOOR}) but reset ${LAST_RESET} has passed; continuing"
    LAST_REMAINING=$RATE_FLOOR
    return 0
  fi
  echo "pr-wait: graphql rate limit low (${LAST_REMAINING} points remaining, floor ${RATE_FLOOR}); sleeping ${wait_for}s until ${LAST_RESET}"
  sleep "$wait_for"
  start=$((start + wait_for))
  LAST_REMAINING=""
  LAST_RESET=""
  read_rate_limit
  if [ "$LAST_REMAINING" -lt "$RATE_FLOOR" ]; then
    die "graphql rate limit still ${LAST_REMAINING} after waiting for reset (floor ${RATE_FLOOR})"
  fi
}

warn_truncated() {
  if [ "$1" = true ]; then
    echo "pr-wait: warning: $2" >&2
  fi
}

# A URL carries its own owner, name and number, so it needs no extra request.
# --repo wins when both are present. A branch name (or no argument) is resolved
# once, up front, not on every poll.
case "$PR" in
  http://github.com/*|https://github.com/*|http://www.github.com/*|https://www.github.com/*)
    pr_path="${PR%%\?*}"
    pr_path="${pr_path%%#*}"
    if [[ "$pr_path" =~ github\.com/([^/]+)/([^/]+)/pull/([0-9]+) ]]; then
      if [ "$REPO_EXPLICIT" -eq 0 ]; then
        REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
      fi
      PR="${BASH_REMATCH[3]}"
    fi
    ;;
esac

if [ -z "$REPO" ]; then
  REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null)" || true
fi
[ -n "$REPO" ] || die "not in a GitHub repo; pass --repo OWNER/NAME"

if [[ ! "$PR" =~ ^[0-9]+$ ]]; then
  if [ -n "$PR" ]; then
    meta="$(gh_try "pr view" pr view "$PR" --repo "$REPO" --json number)"
  else
    meta="$(gh_try "pr view" pr view --repo "$REPO" --json number)"
  fi
  if jq -e '(.errors // []) | length > 0' >/dev/null <<<"$meta"; then
    die "pr view failed: $(jq -r '[(.errors // [])[].message] | join("; ")' <<<"$meta")"
  fi
  PR="$(jq -r '.number // empty' <<<"$meta")"
  [[ "$PR" =~ ^[0-9]+$ ]] || die "could not resolve a pull request number"
fi

owner="${REPO%%/*}"
repo_name="${REPO#*/}"
if [ -z "$owner" ] || [ "$owner" = "$REPO" ] || [ -z "$repo_name" ]; then
  die "repo must be OWNER/NAME (got '${REPO}')"
fi

banner_done=0
checks='[]'
reviews='[]'
threads='[]'
comments='[]'
mergeable="UNKNOWN"
merge_state="UNKNOWN"
number="$PR"
url=""
base=""
state=""
sha=""
total=0
pending=0
start=$(now)
last_sha=""
stable_since=""
sig_prev=""

while :; do
  guard_rate_limit
  raw="$(gh_try "poll" api graphql -f query="$POLL_QUERY" -f owner="$owner" -f name="$repo_name" -F number="$number")"
  if jq -e '(.errors // []) | length > 0' >/dev/null <<<"$raw"; then
    die "poll failed: $(jq -r '[(.errors // [])[].message] | join("; ")' <<<"$raw")"
  fi
  if ! jq -e '.data.repository.pullRequest != null' >/dev/null <<<"$raw"; then
    die "poll returned no pull request ${number} in ${REPO}"
  fi
  parsed="$(jq -c "$PARSE_JQ" <<<"$raw")" || die "could not parse poll response"
  note_rate_limit "$(jq -r '.remaining // empty' <<<"$parsed")" "$(jq -r '.resetAt // empty' <<<"$parsed")"

  url="$(jq -r '.url // empty' <<<"$parsed")"
  base="$(jq -r '.base // empty' <<<"$parsed")"
  state="$(jq -r '.state // empty' <<<"$parsed")"
  sha="$(jq -r '.sha // empty' <<<"$parsed")"
  if [ -z "$url" ] || [ -z "$sha" ] || [ -z "$state" ]; then
    die "poll response missing pull request fields"
  fi
  if [ "$banner_done" -eq 0 ]; then
    echo "pr-wait: $url  ($state, base $base)"
    banner_done=1
  fi
  commit_oid="$(jq -r '.commit // empty' <<<"$parsed")"
  if [ -n "$commit_oid" ] && [ "$commit_oid" != "$sha" ]; then
    echo "pr-wait: warning: head ${sha} differs from the commit that carries checks (${commit_oid})" >&2
  fi

  if [ "$sha" != "$last_sha" ]; then
    [ -n "$last_sha" ] && echo "pr-wait: new head $sha — restarting the wait"
    last_sha="$sha"; start=$(now); stable_since=""; sig_prev=""
  fi

  checks="$(jq -c '.checks' <<<"$parsed")"
  reviews="$(jq -c '.reviews' <<<"$parsed")"
  threads="$(jq -c '.threads' <<<"$parsed")"
  comments="$(jq -c '.comments' <<<"$parsed")"
  mergeable="$(jq -r '.mergeable' <<<"$parsed")"
  merge_state="$(jq -r '.merge_state' <<<"$parsed")"
  warn_truncated "$(jq -r '.checks_more' <<<"$parsed")" "more than 100 check contexts on ${sha}; the digest lists the first 100"
  warn_truncated "$(jq -r '.threads_more' <<<"$parsed")" "more than 100 review threads; the digest lists the first 100"
  warn_truncated "$(jq -r '.reviews_more' <<<"$parsed")" "more than 100 reviews; the digest lists the first 100"
  warn_truncated "$(jq -r '.comments_more' <<<"$parsed")" "more than 100 issue comments; the digest lists the first 100"

  total="$(jq 'length' <<<"$checks")"
  pending="$(jq '[.[] | select(.status != "completed")] | length' <<<"$checks")"
  sig="$(jq -r '[.[] | "\(.id):\(.status)"] | sort | join(",")' <<<"$checks")"
  t=$(now)
  elapsed=$((t - start))
  if [ "$NOWAIT" -eq 1 ]; then break; fi
  if [ "$total" -gt 0 ] && [ "$pending" -eq 0 ]; then
    # every listed run is done — but only trust the list once it has stopped changing
    if [ "$sig" != "$sig_prev" ] || [ -z "$stable_since" ]; then stable_since=$t; fi
    if [ $((t - stable_since)) -ge "$SETTLE" ]; then break; fi
  else
    stable_since=""
  fi
  if [ "$total" -eq 0 ] && [ "$elapsed" -ge "$GRACE" ]; then
    echo "pr-wait: no check runs registered after ${GRACE}s — nothing to wait for (verify the repo has CI/bots before treating this as green)"; break
  fi
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "pr-wait: timed out after ${TIMEOUT}s with $pending/$total check(s) still running"; exit 2
  fi
  sig_prev="$sig"
  if [ "$pending" -gt 0 ] || [ "$total" -eq 0 ]; then
    names="$(jq -r '[.[] | select(.status != "completed") | .name] | join(", ")' <<<"$checks")"
    echo "pr-wait: ${elapsed}s  waiting on $pending/$total: ${names:-(registering)}"
  else
    echo "pr-wait: ${elapsed}s  all $total run(s) complete — settling ($((t - stable_since))/${SETTLE}s)"
  fi
  sleep "$INTERVAL"
done

echo
echo "== CHECKS ($sha)"
jq -r '.[] | "\(.conclusion // .status)\t\(.name)\t\(.output.title // "")"' <<<"$checks" | sort | column -t -s $'\t' 2>/dev/null \
  || jq -r '.[] | "\(.conclusion // .status)\t\(.name)"' <<<"$checks"
failed="$(jq '[.[] | select(.status == "completed" and (.conclusion | IN("failure","cancelled","timed_out","action_required","startup_failure")))] | length' <<<"$checks")"

echo
echo "== REVIEWS"
jq -r '.[] | "\(.submitted_at) \(.user.login) \(.state)\n    \((.body // "") | gsub("\r";"") | .[0:600] | gsub("\n";"\n    "))"' <<<"$reviews" \
  || die "could not format reviews"
[ "$(jq 'length' <<<"$reviews")" -gt 0 ] || echo "(none)"

echo
echo "== REVIEW THREADS (unresolved first)"
jq -r 'sort_by(.isResolved) | .[] | "--- [\(if .isResolved then "resolved" else "OPEN" end)\(if .isOutdated then ", outdated" else "" end)] \(.path):\(.line // "?")\n" + ([.comments.nodes[] | "  \(.author.login): \(.body | gsub("\r";"") | .[0:900] | gsub("\n";"\n    "))"] | join("\n"))' <<<"$threads" \
  || die "could not format review threads"
[ "$(jq 'length' <<<"$threads")" -gt 0 ] || echo "(none)"
unresolved="$(jq '[.[] | select(.isResolved | not)] | length' <<<"$threads")"

echo
echo "== COMMENTS"
jq -r '.[] | "--- \(.created_at) \(.user.login)\n  \(.body | gsub("\r";"") | .[0:900] | gsub("\n";"\n  "))"' <<<"$comments" \
  || die "could not format comments"
[ "$(jq 'length' <<<"$comments")" -gt 0 ] || echo "(none)"

echo
echo "SUMMARY pr=$number checks_total=$total checks_pending=$pending checks_failed=$failed unresolved_threads=$unresolved comments=$(jq 'length' <<<"$comments") state=$state mergeable=$mergeable merge_state=$merge_state"
if [ "$failed" -eq 0 ]; then
  exit 0
fi
exit 1
