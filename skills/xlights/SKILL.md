---
name: xlights
description: Create, edit, inspect, validate and render xLights light-show sequences (.xsq) and show folders (xlights_rgbeffects.xml layout, xlights_networks.xml controllers, .xtiming, .fseq). Use for anything involving xLights, pixel/LED Christmas or Halloween displays, sequencing a song to lights or building non-musical looping animations, effects (Bars, Spirals, Color Wash, Twinkle, Singing Faces...), timing tracks, beats, lyrics, model groups and submodels, colour palettes for RGB pixels, gamma and dimming curves, value curves, layer blending, Falcon Player (FPP) uploads/playlists or xSchedule playback, or the xLights automation/REST/MCP API. Has the exact XML formats, a full per-effect setting-key reference, a Python helper to build and validate sequences, LED colour guidance, and design advice for beginners and experienced sequencers.
---

# xLights sequences and shows

xLights is a free sequencer for computer-controlled light displays. A **show folder** holds the layout
(models = props), controller config, and sequences. A **sequence** (`.xsq`, XML) places **effects** on
**models/groups** along a timeline. A sequence is either a **musical** sequence synced to a song via
**timing tracks**, or a **non-musical animation** (no audio) that usually loops all evening. Many
displays run only animations, so don't assume music. Ask. xLights **renders** each sequence to a `.fseq`,
which **Falcon Player (FPP)** (most common) or xSchedule plays on the lights.

## Golden rules

1. **Look before you write.** Read the layout first (`scripts/xsq.py layout SHOWDIR`). Model and group
   names in a sequence must match the layout **exactly**. Open an existing sequence with
   `scripts/xsq.py info FILE` before changing it.
2. **xLights must not have the file open.** xLights keeps the sequence and layout in memory and overwrites
   them on save. Ask the user to close the sequence (or xLights), or drive the running app through the
   automation API (`references/automation.md`).
3. **Back up first.** `Sequence.save()` writes a timestamped `*.agentbak` copy automatically. For the layout
   or networks XML, copy the file yourself. Never delete the user's `Backup/` or `.xbkp` files.
4. **Never hand-edit `.fseq`.** It's render output. Re-render instead.
5. **Validate after every edit**: `scripts/xsq.py validate FILE --show SHOWDIR` must report 0 errors.
   Then render (`scripts/xsq.py render FILE --show SHOWDIR`) if xLights is installed, and remind the user
   that the player only sees the `.fseq`: re-render, then re-upload to FPP (FPP Connect).
6. **Use the generated reference for setting keys**, never guessed names: `scripts/xsq.py effect NAME`
   or `references/effects/<Name>.md`. Wrong keys are silently ignored.
7. **Ask about hardware-affecting actions** (turning lights on, uploading to controllers, changing the
   show folder) before doing them.

## Which reference to read

| Task | Read |
|---|---|
| Understand or edit `.xsq` structure | `references/xsq-format.md` |
| Effect settings, palettes, value curves, layer blending, transitions, buffers | `references/effect-settings.md` |
| Keys/defaults/ranges for one effect | `references/effects/<Name>.md` (index: `references/effects/README.md`), or `xsq.py effect NAME` |
| Layout, models, groups, submodels, faces, states, controllers | `references/show-files.md` |
| Beats, timing tracks, lyrics/phonemes, `.xtiming` | `references/timing-and-lyrics.md` |
| Making it look good: planning, composition, layering recipes, workflow | `references/sequencing-guide.md` |
| Non-musical animations: looping ambient looks, seamless loops, rotating playlists | `references/animations-and-ambient.md` |
| Falcon Player: FPP Connect uploads, playlists, schedules, troubleshooting playback | `references/falcon-player.md` |
| Colour on real LEDs: RGB mixing, gamma, dimming, palettes that work on *their* lights | `references/color-and-leds.md` |
| Headless render, REST/xlDo commands, MCP server, Lua | `references/automation.md` |

## The format in 60 seconds

```xml
<xsequence ... FixedPointTiming="1" ModelBlending="true">
  <head> ... <sequenceTiming>50 ms</sequenceTiming> <mediaFile>Audio/song.mp3</mediaFile>
         <sequenceDuration>185.000</sequenceDuration> ... </head>
  <ColorPalettes><ColorPalette>C_BUTTON_Palette1=#FF0000,C_CHECKBOX_Palette1=1,...</ColorPalette></ColorPalettes>
  <EffectDB><Effect>E_CHOICE_Bars_Direction=up,E_SLIDER_Bars_BarCount=1,T_CHOICE_LayerMethod=Normal,...</Effect></EffectDB>
  <DataLayers>...Nutcracker...</DataLayers>
  <DisplayElements>                        <!-- rows; every ElementEffects element needs one -->
    <Element type="timing" name="Beats" visible="1" collapsed="0" views="Master View" active="1"/>
    <Element type="model"  name="Mega Tree" visible="1" collapsed="0"/>
  </DisplayElements>
  <ElementEffects>
    <Element type="timing" name="Beats"><EffectLayer><Effect label="" startTime="0" endTime="500"/>...</EffectLayer></Element>
    <Element type="model" name="Mega Tree">
      <EffectLayer>  <!-- layer 0 = TOP -->
        <Effect ref="0" name="Bars" startTime="0" endTime="5000" palette="0"/>
      </EffectLayer>
    </Element>
  </ElementEffects>
  <lastView>0</lastView><TimingTags>...10 Tag elements...</TimingTags>
</xsequence>
```

- Times are **integer ms**, multiples of the frame time, `start < end`, **no overlaps within a layer**.
- `ref` indexes `<EffectDB>` (E_/T_/B_ keys); `palette` indexes `<ColorPalettes>` (C_ keys). Append new
  entries and never renumber existing ones.
- Values escape `&`→`&amp;` then `,`→`&comma;` before XML escaping.
- `EffectDB`/`ColorPalettes`/`DisplayElements` must come **before** `ElementEffects` (single-pass loader).
- Layers composite bottom-up. An upper layer's `T_CHOICE_LayerMethod` mixes it over everything below.

## Helper script: `scripts/xsq.py` (Python 3.9+, stdlib only)

Run from the skill directory, or put `scripts/` on `sys.path` to import it.

```bash
python3 scripts/xsq.py layout   "/path/Show"                       # models, groups, submodels, faces
python3 scripts/xsq.py info     "/path/Show/Song.xsq" [-v]         # what's in a sequence
python3 scripts/xsq.py validate "/path/Show/Song.xsq" --show "/path/Show"
python3 scripts/xsq.py effect   Bars [--all]                       # keys, defaults, ranges, options
python3 scripts/xsq.py new      "/path/Show/New.xsq" --duration 185 --media Audio/song.mp3 --models "Mega Tree,Arches"
python3 scripts/xsq.py add-effect "/path/Show/New.xsq" --model "Mega Tree" --effect Spirals \
        --start 0 --end 8000 --layer 0 --set E_SLIDER_Spirals_Count=3 --colors "#FF0000,#FFFFFF"
python3 scripts/xsq.py add-timing "/path/Show/New.xsq" --name Beats --marks 0,500,1000,1500
python3 scripts/xsq.py vc Bars Bars_Cycles Ramp 10 50              # value-curve setting string
python3 scripts/xsq.py color-test "/path/Show/Color Test.xsq" --show "/path/Show" --colors "#FF3000,#6000FF,#FFB060"
python3 scripts/xsq.py render   "/path/Show/New.xsq" --show "/path/Show"   # headless render to .fseq
```

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from xsq import Sequence, load_layout, value_curve

seq = Sequence.new(duration_s=185, frame_ms=50, media="Audio/song.mp3", song="...", artist="...")
# or: seq = Sequence.load("/path/Show/Song.xsq")
seq.add_timing("Beats", marks=[0, 476, 952, 1428])          # boundaries, or [(start, end, label), ...]
seq.add_timing("Lyrics", layers=[phrases, words, phonemes])  # lyric track (3 layers)
seq.add_model("Mega Tree")                                    # exact layout name (model or group)
k, v = value_curve("Bars", "Bars_Cycles", "Ramp", 10, 50)    # raw units: 1.0 -> 5.0 cycles
seq.add_effect("Mega Tree", "Bars", 0, 8000, layer=0,
               settings={"E_CHOICE_Bars_Direction": "down", k: v, "T_TEXTCTRL_Fadeout": "0.50"},
               colors=["#FF0000", "#00FF00"], palette={"C_SLIDER_Brightness": 60})
seq.add_effect("Arches", "On", 0, 500, submodel="Arch 1")    # SubModelEffectLayer
for fx in seq.iter_effects(): ...                            # decoded settings/palette per effect
seq.clear_effects("Mega Tree", layer=0, start=0, end=8000)
fx = next(f for f in seq.iter_effects() if f["model"] == "Arches" and f["name"] == "On")
seq.update_effect(fx["node"], settings={"T_TEXTCTRL_Fadeout": "1.00"}, end=6000)  # edit in place
seq.save("/path/Show/Song.xsq")                              # writes Song.<timestamp>.agentbak first
```

`add_effect` fills in the effect's full default settings (like xLights does), snaps times to the frame
grid, de-duplicates EffectDB/palette entries, and refuses overlaps. Effect names are case and space
tolerant (`colorwash` becomes `Color Wash`).

## Typical workflows

**New sequence for a song**: ask for the audio file, the props that matter, mood, and existing timing.
Read the layout. Create the sequence with `--media` and the real duration. Build timing tracks
(`timing-and-lyrics.md`). Plan sections and energy, then place base, feature, and accent layers
(`sequencing-guide.md`). Validate, render, and summarise what you made and what the user should review.

**New animation (no music)**: ask which props, the feel (calm, festive, spooky), the loop length, and
whether it'll rotate with other looks. `xsq.py new OUT --duration 60 --models ...` (no `--media` gives
`sequenceType` Animation). Build a base layer plus a texture spanning the whole loop with whole-number
cycle counts so it loops seamlessly (`animations-and-ambient.md`). Validate, render, and explain how to
add it to a repeating FPP playlist.

**Get it onto the lights**: render, then upload with FPP Connect (sequence, media for musical shows,
target playlist). Uploads affect live hardware, so describe what will be sent and let the user run it or
approve it (`falcon-player.md`).

**Edit an existing sequence**: `info` it, make targeted changes with `Sequence.load` + `update_effect` (change an
effect's settings in place) / `add_effect` / `clear_effects`, save (auto backup), validate, render.

**Fix a broken sequence**: `validate --show`, which reports missing models, bad refs, overlaps, bad timing
track references, unknown keys, and canvas mistakes. Fix the causes, not the symptoms. For renamed
models, rename the element in the sequence (both DisplayElements and ElementEffects) or add an
`oldname:` alias in the layout.

**Colours look wrong on the lights**: read `color-and-leds.md`. Build a `color-test` sequence, have the
user watch it on the real display at night, and tune palettes and gamma.

**Layout or controller changes**: prefer the xLights UI. If editing XML, follow `show-files.md`.

## Talking to users

- Many users are new. Explain terms briefly the first time (model, group, layer, timing track, render)
  and say what you changed in plain language: "Added a red/white Spirals on the Mega Tree for the first
  chorus (0:45–1:05), on top of the existing wash."
- Don't overpromise taste. Generated sequences are a starting point, so invite the user to watch and tweak.
- When unsure about something you can't see (how colours look on their pixels, which props are most
  visible from the street, whether timing feels right), ask.
- Experienced users want specifics: exact keys, layer methods, buffer styles, value-curve parameters.
  The references have them.
