#!/usr/bin/env bash
# Print the tag of the latest *stable* xLights release (e.g. "2026.19").
#
# Source of truth: the GitHub Release marked "Latest" (excludes drafts and pre-releases such as
# "nightly"). Set GH_TOKEN/GITHUB_TOKEN to avoid API rate limits. If the API is unreachable, falls
# back to the highest YYYY.N[.N] tag, with a warning on stderr (that tag may not be published yet).
set -euo pipefail
REPO=xLightsSequencer/xLights

auth=()
token="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
[[ -n "$token" ]] && auth=(-H "Authorization: Bearer $token")

if json=$(curl -fsSL ${auth[@]+"${auth[@]}"} -H "Accept: application/vnd.github+json" \
            "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null); then
  tag=$(printf '%s' "$json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')
  if [[ -n "$tag" ]]; then
    echo "$tag"
    exit 0
  fi
fi

echo "warning: GitHub releases API unavailable; falling back to highest version tag" >&2
git ls-remote --tags --refs "https://github.com/$REPO.git" \
  | sed 's#.*refs/tags/##' \
  | grep -E '^[0-9]{4}\.[0-9]+(\.[0-9]+)?$' \
  | sort -V | tail -1
