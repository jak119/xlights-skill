# Scenario evals for the xLights skill

Use these to judge the skill end to end with a fresh agent that has only the installed skill (not this
repo's maintainer context). Run each against a **copy** of a test show folder (for example
`tests/fixtures/show`, or a sanitized real show with groups, submodels and a face).

```bash
mkdir -p /tmp/xl-eval && cd /tmp/xl-eval && git init -q
npx skills add /path/to/xlights-skill --copy -y
cp -R /path/to/test-show ./show
# then start the agent in /tmp/xl-eval and paste a scenario prompt
```

## Universal rubric (apply to every scenario)

| # | Check | How to verify |
|---|---|---|
| U1 | Read the layout before writing; used exact model names | Transcript; `xsq.py validate --show` reports no missing models |
| U2 | No guessed setting keys | `validate` shows no "unrecognised key" warnings |
| U3 | Output validates with 0 errors | `python3 <skill>/scripts/xsq.py validate FILE --show show` |
| U4 | Renders in real xLights (if available) | `xLights --headless -s show FILE` exits 0; log has no "Effect dropped" |
| U5 | Didn't modify files the task didn't ask about; backups exist for edited files | `git status` / file list; `*.agentbak` present |
| U6 | Explained the result in plain language (what, where, when) and what to review | Final message |
| U7 | Asked before hardware-affecting actions (uploads, lights on) | Transcript |

## Scenarios

**S1. Beginner animation (no music)**
> "I'm new to xLights. Make me a calm 60-second looping animation for my porch lights in orange and purple for Halloween."

Pass: `sequenceType` Animation with no media. Effects span 0–60000 on every base layer. Whole-number
cycle counts or random textures (loop-friendly). Brightness is moderate. Beginner-friendly explanation
of how to loop it on FPP.

**S2. Musical sequence skeleton**
> "Start a sequence for `Audio/song.mp3` (3:05, 120 BPM, first downbeat at 0.5 s). Add beat and bar timing tracks and a song-structure track with intro 0–15 s, verse 15–45 s, chorus 45–75 s."

Pass: duration 185 s, `Media` type, beats every 500 ms from 500 ms, bars every 2000 ms, structure labels
correct. Times snapped to the frame grid. The agent notes that fixed-BPM timing may drift.

**S3. Layered effect with blending**
> "On the Single Line, put a slow red/green Color Wash for the whole sequence and white twinkles on top of it."

Pass: wash on a lower layer, Twinkle on layer 0 above it, `Normal` (or a justified) layer method. The
palettes are correct (the twinkle palette has only white enabled).

**S4. Edit an existing sequence**
> "In Testing.xsq, make the chase on Single Line go right-to-left and add a 1-second fade-out."

Pass: changes the existing effect's settings (`E_CHOICE_Chase_Type1=Right-Left`,
`T_TEXTCTRL_Fadeout=1.00`) rather than stacking a duplicate. Other effects are untouched. Backup made.

**S5. Value curve**
> "Make the Bars on the tree speed up from 1 to 5 cycles over the effect."

Pass: `E_VALUECURVE_Bars_Cycles` with `Min=0.00|Max=300.00`, P1=10, P2=50, `RV=TRUE` (raw units).
Rendering shows motion speeding up.

**S6. Fix a broken sequence**
> "xLights says some of my models are missing when I open Layered.xsq. Fix it."

Pass: identifies that `String 1` is an old-name alias of `Single Line`, renames it in **both**
DisplayElements and ElementEffects, and the file validates with no warnings for it.

**S7. Colours look wrong**
> "My orange looks yellow and my white looks blue on my bullet pixels."

Pass: explains why (die efficiency, gamma), suggests hex adjustments (lower green for orange; reduce blue
for white), offers a `color-test` sequence, and mentions controller or model gamma and dimming curves
as the hardware-level fix. No claim that the screen colour is "right".

**S8. Getting it onto FPP**
> "I rendered my new sequence. How do I get it playing on my Falcon Player every night?"

Pass: re-render → FPP Connect (sequence, media only for musical, FSEQ V2 Sparse/zstd, playlist) →
FPP web UI playlist repeat and schedule. Warns that Upload Outputs and Models can restart FPPD.
Doesn't upload without permission.

**S9. Expert detail**
> "What layer method should I use so a white Text effect on top only shows the plasma underneath through the letters?"

Pass: recommends `1 is Unmask` (or `1 is True Unmask`) on the Text layer (the upper layer), explains
that the method lives on the upper layer, and gives the exact key `T_CHOICE_LayerMethod`.

**S10. Refuse to guess**
> "Add a Shader effect using my file Shaders/foo.fs with speed 2."

Pass: uses `E_0FILEPICKERCTRL_IFS` / `E_SLIDER_Shader_Speed` (divisor 100, so 200) per the reference, or
recommends configuring shader parameters in the UI because they're dynamic. Doesn't invent keys.

## Recording results

For each run, note the skill commit, the agent/model, pass/fail per rubric item, and any wrong facts the
agent stated. Turn recurring failures into either a doc fix (missing or unclear guidance) or a test
(a factual error in the skill).
