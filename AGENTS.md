# AGENTS.md: maintaining the xLights skill

This repo packages one Agent Skill, `skills/xlights/`, that teaches agents to create, edit, validate and
render xLights shows. This file is for agents (and humans) **maintaining** the skill. The skill's own
instructions for end users are in `skills/xlights/SKILL.md`.

xLights changes fast (several releases a year, new effects, new file sections, new automation APIs).
**The skill tracks the latest stable xLights release** (the GitHub Release marked "Latest", currently
the version in `data/effects.json` → `_release`), never `master` or `nightly`. Users run releases, and
documenting unreleased behaviour would mislead them.
The skill's value depends on being **exactly right** about formats and setting keys, so every change here
should be checked against the xLights source or real files, never written from memory.

## Repo layout

| Path | What | Edit? |
|---|---|---|
| `skills/xlights/SKILL.md` | Entry point: rules, workflows, helper usage. Keep it lean (≲200 lines); details go in `references/`. | By hand |
| `skills/xlights/references/*.md` | Hand-written references (formats, settings, design, colour, timing, animations, FPP, automation) | By hand, verified against source |
| `skills/xlights/references/effects/` | One page per effect + `README.md` index | **Generated, don't edit** |
| `skills/xlights/data/effects.json` | Machine-readable key table used by `xsq.py` | **Generated, don't edit** |
| `skills/xlights/scripts/xsq.py` | Helper CLI and library. Python ≥3.9, **stdlib only** (it runs wherever the skill is installed) | By hand |
| `tools/build_effect_reference.py` | Generator for the two generated outputs. Holds `SHARED_CUSTOM_KEYS` / `EXTRA_EFFECT_KEYS` for keys the metadata can't describe | By hand |
| `tools/update_from_upstream.sh` | Shallow-clone or update xLights, regenerate, test, summarise | By hand |
| `tests/test_skill.py` | Offline tests + optional real-xLights integration tests | By hand |
| `tests/fixtures/show/` | Small sanitized show: xLights-written `Testing.xsq`, a layered `Layered.xsq`, a trimmed layout | Add fixtures, keep them sanitized |
| `evals/scenarios.md` | Task scenarios for judging the skill end to end | By hand |

## Everyday commands

```bash
python3 tests/test_skill.py                                   # offline tests (must pass before any commit)
XLIGHTS_SHOW="/path/to/a/show" python3 tests/test_skill.py    # + render tests with real xLights
XLIGHTS_SKILL_EXTRA_SHOWS="/show1:/show2" python3 tests/test_skill.py   # check keys in more real sequences
tools/update_from_upstream.sh                                 # refresh from the latest stable release (shallow clone)
tools/latest_xlights_release.sh                               # print that release's tag
npx skills add . --list                                       # confirm the skill is discoverable
```

The integration tests only create files named `zz skilltest *` in `XLIGHTS_SHOW` and delete them
afterwards. On macOS the show folder must be one xLights has already opened (sandbox), and the binary
is auto-found at `/Applications/xLights.app/Contents/MacOS/xLights` (or set `XLIGHTS_BIN`).

## CI (GitHub Actions)

| Workflow | When | What it guarantees |
|---|---|---|
| `.github/workflows/test.yml` → `unit` | push / PR | Offline tests pass on Python 3.9 and 3.13 (`xsq.py` stays stdlib-only and 3.9-compatible). |
| `test.yml` → `skills-cli` | push / PR | `npx skills add` discovers the skill, and an installed copy has `data/` + `references/` and runs. |
| `test.yml` → `generated-fresh` | push / PR | The recorded `_release` is a real release tag whose commit equals `_commit`, and regenerating from it reproduces the committed files exactly. So the reference really describes a stable release, nobody hand-edited generated output, and generator changes were re-run. Uses a ~2 MB sparse, blob-filtered fetch of just `resources/effectmetadata`. |
| `.github/workflows/upstream-sync.yml` | weekly + manual | Resolves the latest stable release (`tools/latest_xlights_release.sh`, GitHub releases API) or a chosen tag, refuses `master`/`nightly`, regenerates, runs tests, and opens a `bot/xlights-sync-<release>` PR with a review checklist when something changed. Needs "Allow GitHub Actions to create and approve pull requests" enabled in repo settings. |

The skills CLI installs straight from the repo's default branch (`npx skills add <owner>/<repo>`;
`npx skills update` pulls new commits), so there's **no publish step**. Keep `main` green: protect it
and require the `Test` workflow. Integration tests need a real xLights binary, so they don't run in CI.
Run them locally before merging sync PRs that change behaviour.

When you change the generator, re-run it against the **recorded** release in the same PR, or
`generated-fresh` fails:

```bash
REL=$(python3 -c "import json;print(json.load(open('skills/xlights/data/effects.json'))['_release'])")
XLIGHTS_REF="$REL" tools/update_from_upstream.sh
```

## Getting the xLights source to reference

Use a **shallow, untracked** checkout under `.cache/` (gitignored). Never vendor xLights into this repo.

```bash
TAG=$(tools/latest_xlights_release.sh)      # latest stable release, e.g. 2026.19
git clone --depth 1 --branch "$TAG" https://github.com/xLightsSequencer/xLights.git .cache/xLights
# smaller, metadata only (what the generator needs):
#   git clone --depth 1 --filter=blob:none --sparse --branch "$TAG" <url> .cache/xLights
#   git -C .cache/xLights sparse-checkout set --no-cone /resources/effectmetadata/ /src-core/xLightsVersion.h
```

`tools/update_from_upstream.sh` does this for you. Look at `master` only to **preview** what's coming
(`XLIGHTS_REF=master tools/update_from_upstream.sh`, then discard the changes). Don't document
unreleased behaviour; if you must mention it, say "coming after <release>". The xLights repo has its own `AGENTS.md` describing
its layout (`src-core/` is the shared, wx-free core; `src-ui-wx/` is the desktop UI). Read it when
you need to find something.

## Updating for a new xLights release

1. **Refresh**: `tools/update_from_upstream.sh` (defaults to the latest stable release; or
   `tools/update_from_upstream.sh /path/to/checkout TAG`). Note the release and commit it prints.
2. **Review generated diffs** (`git diff --stat skills/xlights/data skills/xlights/references/effects`):
   - **New effect** → read its `src-core/effects/<Name>Effect.cpp`. Any `"custom"` controls in its metadata
     hide real keys; grep the `.cpp` for `"E_…"` / `"CHOICE_…"` strings and add them to
     `EXTRA_EFFECT_KEYS` in the generator. Re-run.
   - **Removed or renamed keys** → check `RemapChangedSettingKey` / `ControlRenameMap`
     (`src-core/render/Effect.cpp`) to see whether old files still load. Update any examples in the
     hand-written references that use them (`grep -rn KEY skills/`).
   - **Key derivation changed** → compare `JsonEffectPanel.cpp` (search `ID_SLIDER_`, `ID_FILEPICKERCTRL_`,
     `settingPrefix`, `suppressKeys`) with `control_prefix()` in the generator. The desktop is the source
     of truth (the iPad Swift mapping differs for picker controls).
3. **Re-verify the hand-written facts** in the provenance map below that touch changed upstream files.
   Diff those files between the previous release (`_release` before your change) and the new one,
   for example with two sparse clones at both tags. Fix the reference text if behaviour changed.
4. **Check new capabilities**: `xLights --help` (CLI flags), `documentation/xlDo Commands.txt`
   (automation commands, MCP tools), new top-level `.xsq` sections in `SequenceFile::BuildDocument`
   (update `SECTION_ORDER` in `xsq.py` and `xsq-format.md`), FPP Connect options
   (`src-ui-wx/controllers/FPPConnectDialog.cpp`, `AddInstanceHeader` tooltips).
5. **Bump version mentions**: `Sequence.new(version=...)` default in `xsq.py`, the release line in
   `README.md`, and "verified with 2026.xx" notes in references (`grep -rn "2026\." skills README.md`).
6. **Test**: offline tests, then integration tests against an install of **that release**, then
   `npx skills add . --list`. If you can, run a couple of `evals/scenarios.md` tasks.
7. **Record** what changed in the commit message (xLights release and commit, effects added, facts
   re-verified or corrected).

## Provenance map (where each hand-written fact comes from)

When a fact is in doubt, re-derive it from these locations (paths relative to the xLights repo).

| Fact (reference file) | Source of truth | How to re-check |
|---|---|---|
| `.xsq` element/attribute names, section order (`xsq-format.md`) | `src-core/render/SequenceFile.cpp` `BuildDocument`, `WriteEffectsPugi`, `LoadSequence` | Read the writer; save a sequence in xLights and diff |
| Single-pass load; ElementEffects needs DisplayElements; effect dropped if start ≥ end; times rounded to frames | `src-core/render/SequenceElements.cpp` `LoadSequencerFile`, `LoadEffects` | Read; the validator tests encode these |
| Settings string escaping `&amp;` / `&comma;` | `src-core/utils/UtilClasses.h` `AsString`, `UtilClasses.cpp` `Parse` | `test_build_and_round_trip` |
| Key = prefix + control + `_` + id; float slider → TEXTCTRL unless `settingPrefix` | `src-ui-wx/effectpanels/JsonEffectPanel.cpp` | Generator + `test_every_fixture_key_is_known` |
| `C_` keys in palette, others in EffectDB | `src-core/render/Effect.cpp` `ApplySetting` | Real files (palette has `C_SLIDER_Brightness`) |
| Value curve string, Min/Max raw units, `RV=TRUE`, output ÷ divisor (`effect-settings.md`) | `src-core/render/ValueCurve.cpp` `Serialise`/`Deserialise`/`GetOutputValueAtDivided`; `src-core/effects/RenderableEffect.cpp` | **`test_value_curve_units` (render proof)** |
| Value-curve P1–P4 meanings per type | `src-ui-wx/shared/dialogs/ValueCurveDialog.cpp` (label switch) | Only Flat/Ramp semantics are render-verified |
| Layer order (layer 0 top, composite bottom-up), mix-method semantics | `src-core/render/PixelBuffer.cpp` `GetMixedColor`, `mixColors`, `MixTypesMap` | Read the switch |
| Transition types, layer-method list | `src-ui-wx/sequencer/BlendingPanel.cpp` | Read the arrays |
| Buffer styles | `src-core/models/Model.cpp` `DEFAULT_BUFFER_STYLES`, `src-core/models/ModelGroup.cpp` | Read |
| Missing models: GUI prompt, `oldname:` alias auto-rename, batch/headless drops | `src-ui-wx/sequencer/tabSequencer.cpp` `CheckForValidModels` | Read |
| Layout XML names (models, groups, submodels, faces, states, aliases) (`show-files.md`) | `src-core/XmlSerializer/XmlNodeKeys.h`, `BaseSerializingVisitor.cpp` | Read; check against a real `xlights_rgbeffects.xml` |
| Start-channel prefixes `! > @ #` | `src-core/models/Model.cpp` (start-channel parsing) | Read |
| Dimming curve XML and formula (`color-and-leds.md`) | `src-core/render/DimmingCurve.cpp` | Read `BasicDimmingCurve::init`, `createFromInfo` |
| `.xtiming` format (lowercase `starttime`) (`timing-and-lyrics.md`) | `src-core/render/Element.cpp` `TimingElement::GetExport`; `SequenceFile.cpp` `ProcessXTiming` | Read |
| Faces read phoneme layer 2 | `src-core/effects/FacesEffect.cpp` (`GetEffectLayer(2)`) | Read |
| CLI flags, headless exit codes (`automation.md`) | `xLights --help`; xLights `AGENTS.md` "Headless render mode" | Run `--help` |
| REST/xlDo/MCP commands | `documentation/xlDo Commands.txt`, `src-ui-wx/automation/xLightsMCPServer.cpp` | Read |
| FPP Connect options (`falcon-player.md`) | `src-ui-wx/controllers/FPPConnectDialog.cpp` `AddInstanceHeader` tooltips | Read |
| Effect panel defaults/ranges/options | `resources/effectmetadata/*.json` (+ `shared/`) | Generated |

**Verification baseline:** the hand-written references were researched against xLights `master` at
`0757d02` (2026-11-06), then every file in this map was diffed against the **2026.19** release tag.
The differences were bug fixes, plus a new `--fseqhash` CLI flag that the skill doesn't document. None
changes a documented fact. Integration tests ran against an installed 2026.19.

**Known unverified or approximate** (improve these when you can, and say so in docs until then):
- Value-curve P1–P4 semantics for curve types other than Flat/Ramp (from UI labels, not render tests).
- Model-blending order between overlapping rows (docs are hedged).
- `C_SLIDER_ChromaSensitivity` range and `B_CUSTOM_SubBuffer` string format.
- Design advice (`sequencing-guide.md`, `animations-and-ambient.md`, colour palettes) is experience-based
  guidance, not derived from source. Keep it hedged ("starting point", "tune on real lights").
- `xsq.py` refuses files with `<CompressedData>` sections (zstd) rather than inflating them.

## Evaluating the skill

1. **Mechanical**: `python3 tests/test_skill.py` (plus integration). Add a test whenever you fix a bug or
   verify a new fact. Prefer render-based proofs (`--fseqcmp`) for anything about how xLights
   *interprets* a value.
2. **Real-world keys**: run with `XLIGHTS_SKILL_EXTRA_SHOWS` pointing at real show folders (your own,
   or vendor sequences you're licensed to use). Any missing key means a generator gap or a legacy key.
3. **Scenario evals**: install the skill into a scratch project (`npx skills add <repo> --copy -y`), give a
   fresh agent the tasks in `evals/scenarios.md` against a copy of a test show, and grade with the
   rubric there. Watch for guessed keys, unvalidated output, edits to open files, and missing
   explanations for beginners.
4. **Trigger check**: the `description` in SKILL.md frontmatter decides when agents load the skill. Keep
   it under 1024 chars and keyword-rich (xLights, .xsq, pixels, FPP, Christmas/Halloween…).

## Conventions

- Verify, then write. Cite the source file in this map when you add a new fact.
- Hedge anything not verified, and list it under "Known unverified".
- `xsq.py` stays dependency-free and backward compatible (other agents call its CLI). Add flags; don't
  rename them.
- Never commit user show data with personal details (controller IPs, `ShowGUID`, names, addresses).
  Sanitize fixtures as in `tests/fixtures/show/xlights_rgbeffects.xml`.
- Writing style for references: short sections, tables, exact keys in backticks, and examples that pass
  `xsq.py validate`. Beginners read these too, so explain jargon once.
