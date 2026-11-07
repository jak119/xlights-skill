# xLights skill for AI agents

An [Agent Skill](https://agentskills.io) that teaches coding agents (Claude Code, Cursor, Codex, etc.) to
create, edit, validate and render **xLights** light-show sequences and show folders.

Most of this was written with AI (Claude). It works for my show, but no promises it'll work for yours.

It includes:

- **Exact file formats**: `.xsq` sequences, `xlights_rgbeffects.xml` layouts, `xlights_networks.xml`,
  `.xtiming`. Verified against the xLights source and real show files.
- **Every effect's setting keys** (56 effects): types, defaults, ranges, options and descriptions. They're
  generated from xLights's own effect-panel metadata (`references/effects/`, `data/effects.json`).
- **`scripts/xsq.py`**: a dependency-free Python CLI and library to inspect a layout, build sequences,
  add effects, timing tracks and value curves, validate against the layout, create colour-test
  sequences, and headless-render with xLights.
- **Guidance**: sequencing and design advice for beginners and veterans (musical shows and
  non-musical looping animations), Falcon Player (FPP) upload and playback, colour on real LEDs (RGB
  mixing, gamma, dimming curves, per-strand variation, palettes), and automation (CLI, REST, MCP).

## Install

```bash
# from a local checkout
npx skills add /path/to/xlights-skill
# or from GitHub once published
npx skills add jak119/xlights-skill
```

List what the package contains: `npx skills add /path/to/xlights-skill --list`.

## Layout

```
skills/xlights/
  SKILL.md                     entry point (rules, workflows, helper usage)
  references/                  formats, settings, design, colour, timing, automation
  references/effects/          one page per effect (generated)
  data/effects.json            machine-readable effect key table (generated)
  scripts/xsq.py               helper CLI / library (Python 3.9+, stdlib only)
tools/build_effect_reference.py   regenerates the effect reference from an xLights checkout
tools/update_from_upstream.sh     shallow-clone the latest stable xLights release, regenerate, test
tools/latest_xlights_release.sh   print the latest stable release tag (GitHub "Latest" release)
tests/                            offline + optional real-xLights integration tests, sanitized fixtures
evals/scenarios.md                end-to-end scenario evals with a grading rubric
.github/workflows/                CI: tests, skills-CLI install check, upstream sync PRs
AGENTS.md                         maintainer guide for agents (CLAUDE.md points here)
```

## CI

- `Test` (every push/PR): offline tests on Python 3.9 and 3.13, a skills-CLI discover-and-install
  check, and a check that the generated reference matches its recorded stable xLights release.
- `Sync with upstream xLights` (weekly): regenerates from the **latest stable xLights release**
  (never master or nightly) and opens a PR for review.

See `AGENTS.md` for maintainer details.

## Updating the effect reference

When xLights adds or changes effects:

```bash
tools/update_from_upstream.sh          # shallow-clones the latest stable release, regenerates, tests
```

The skill tracks the latest **stable** xLights release. The current reference was generated from
release **2026.19** (`24ec3d4`, 2026-10-23).

## License

[MIT](LICENSE). Not affiliated with the xLights project.
