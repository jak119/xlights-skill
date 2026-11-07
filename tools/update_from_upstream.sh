#!/usr/bin/env bash
# Refresh the skill's generated reference from the latest STABLE xLights release.
#
#   tools/update_from_upstream.sh                    latest stable release -> .cache/xLights (shallow)
#   XLIGHTS_REF=2026.19 tools/update_from_upstream.sh   a specific release tag
#   tools/update_from_upstream.sh /path/xL [TAG]     use an existing checkout (pass the tag it's at)
#
# The skill documents what users actually run, so it tracks published releases, never master.
# To preview upcoming changes without committing them: XLIGHTS_REF=master ... then discard.
#
# Then: regenerates references/effects + data/effects.json, runs the offline tests, and
# prints what changed so you can review it (see AGENTS.md "Updating for a new xLights release").
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="${1:-}"
if [[ -z "$SRC" ]]; then
  SRC=.cache/xLights
  REF="${XLIGHTS_REF:-$(tools/latest_xlights_release.sh)}"
  echo "== Using xLights ref: $REF"
  if [[ -d "$SRC/.git" ]]; then
    git -C "$SRC" fetch --depth 1 origin "refs/tags/$REF:refs/tags/$REF" 2>/dev/null \
      || git -C "$SRC" fetch --depth 1 origin "$REF"
    git -C "$SRC" checkout -q "$REF" 2>/dev/null || git -C "$SRC" checkout -q FETCH_HEAD
  else
    mkdir -p .cache
    git clone --depth 1 --branch "$REF" https://github.com/xLightsSequencer/xLights.git "$SRC"
  fi
else
  REF="${2:-}"
  [[ -z "$REF" ]] && echo "warning: no tag given for $SRC; the reference won't record a release" >&2
fi
[[ "$REF" == "master" || "$REF" == "main" ]] && echo "WARNING: generating from $REF (unreleased). Don't commit this." >&2

echo "== xLights source: $(git -C "$SRC" log -1 --format='%h %cd %s' --date=short)"
grep -h 'xlights_version_string *=' "$SRC/src-core/xLightsVersion.h" || true

python3 tools/build_effect_reference.py "$SRC" ${REF:+--ref "$REF"}
python3 tests/test_skill.py

echo
echo "== Generated-file changes (review these):"
if git rev-parse --git-dir >/dev/null 2>&1; then
  git --no-pager diff --stat -- skills/xlights/data skills/xlights/references/effects || true
  echo
  echo "== Effects added/removed:"
  git --no-pager diff --name-status -- skills/xlights/references/effects | grep -E '^[AD]' || echo "(none)"
else
  echo "(not a git repo - compare manually)"
fi

echo
echo "== Upstream files the hand-written references were verified against (re-check these):"
for f in src-core/render/SequenceFile.cpp src-core/render/SequenceElements.cpp \
         src-core/render/ValueCurve.cpp src-core/render/PixelBuffer.cpp src-core/render/DimmingCurve.cpp \
         src-core/utils/UtilClasses.h src-core/XmlSerializer/XmlNodeKeys.h \
         src-ui-wx/effectpanels/JsonEffectPanel.cpp src-ui-wx/sequencer/BlendingPanel.cpp \
         src-ui-wx/controllers/FPPConnectDialog.cpp "documentation/xlDo Commands.txt" \
         resources/effectmetadata/shared; do
  if [[ -e "$SRC/$f" ]]; then echo "  present: $f"; else echo "  MISSING (moved/renamed?): $f"; fi
done
echo "(Shallow clones have no history. To see what changed since the last sync, diff these files between the\n previous release in git history of data/effects.json ('_release') and this one, e.g. with two sparse clones.)"
