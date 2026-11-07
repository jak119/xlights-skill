# Sequencing guide: making shows that look good

Advice for building light shows in xLights, written for newer sequencers but useful for veterans. Pair it
with the format references when you generate or edit sequences. Most of this guide is about **musical**
sequences. For looping, non-musical animations see `animations-and-ambient.md`. The composition,
layering, and colour advice applies to both.

## 1. Mental model (explain this to new users)

- **Show folder**: one folder per display (layout, controllers, sequences, media).
- **Layout**: the props ("models") and where they sit in the house preview. Sequences reference models
  **by name**.
- **Controllers**: hardware that drives pixels. The layout maps each model to a controller port and channels.
- **Sequence (`.xsq`)**: a timeline. Rows are timing tracks and models/groups. Each row has layers, and each
  layer holds effects with a start and end time.
- **Effect**: a generator (Bars, Spirals, Twinkle…) with settings, a colour palette, blending, and buffer options.
- **Render**: xLights computes every pixel for every frame into a `.fseq`, which is what plays on FPP or
  xSchedule. Edits to an `.xsq` do nothing until the sequence is re-rendered.

## 2. Plan before placing effects

1. **Know the props.** Run `xsq.py layout SHOWDIR`. Note the high-impact "hero" props (mega tree, matrix,
   singing faces, arches, spinners), the outline props (rooflines, windows, mini trees), and the groups.
2. **Listen to the song** and write down its structure with times: intro, verses, pre-chorus, chorus,
   bridge, drops, key hits, ending. Put it in a "Song Structure" timing track.
3. **Map energy to props.** Low energy: few props, slow motion, dim. High energy: everything, fast motion,
   full brightness. Save the "whole house" moment for the biggest chorus or drop.
4. **Choose a palette story.** 2–4 colours per section is plenty. Change palettes at section boundaries,
   not randomly. Classic sets: Christmas red/green/white; warm white + gold; icy blue/white/purple;
   Halloween orange/purple/green.
5. **Make timing tracks first**: beats, bars, song structure, and lyrics for faces. See
   `timing-and-lyrics.md`.

## 3. Composition principles

- **Contrast beats clutter.** The most common beginner mistake is every prop running a busy effect all
  song long. Leave space. Darkness and stillness make the hits land.
- **Lead and support.** At any moment pick a focal prop or group (it gets the interesting motion). Other
  props get a supporting wash, a twinkle, or nothing.
- **Movement should mean something.** Sweep across the yard (group with `Per Preview` buffer) on rising
  phrases, and pulse on the beat with short On/fade effects. Spirals and rotations suit sustained notes.
- **Match the music's texture**:
  - Drums/beats → On with quick fades, Strobe, Shockwave, Fireworks, Bars (short).
  - Melody/vocals → Singing faces, Single Strand chases, Meteors, Wave, Text (lyrics).
  - Pads/sustain → Color Wash, Butterfly, Plasma, Spirals (slow), Twinkle.
  - Builds → value-curve ramps (brightness up, speed up, more bars), Ripple, growing Fan.
  - Drops/hits → whole-house On or Shockwave, then silence.
- **Symmetry and call-and-response**: left/right prop pairs alternating on beats, or the tree answering
  the house.
- **Consistency**: repeated musical sections should have recognisably similar (not identical) looks. You
  can copy a chorus and vary the palette or direction.
- **Transitions**: soft fades (`T_TEXTCTRL_Fadein/Fadeout` 0.25–1 s) between sections avoid jarring
  cuts. Use hard cuts deliberately on hits.
- **Brightness**: pixels at 100% white everywhere are harsh and power-hungry. Use palette brightness 30–70%
  for washes, and keep full brightness for accents. Pure white needs the most power.

## 4. Layering patterns that work

| Goal | Recipe |
|---|---|
| Texture over a base | Bottom: Color Wash (dim). Top: Twinkle or Shimmer, `Normal`. |
| Text/shape filled with a pattern | Bottom: Bars/Plasma/Spirals. Top: Text or Shape in white, `1 is Unmask` (or `Highlight`). |
| Cut-outs | Top layer `1 is Mask`: wherever it's lit, the layers below go dark. |
| Accent hits over everything | Top layer: short Strobe/On on beats, `Normal` or `Max`. |
| Distort what's below | Top: Warp or Kaleidoscope with `T_CHECKBOX_Canvas=1`. |
| Cross-fade two looks | Two layers with `Effect 1`/`Effect 2` and `T_CHECKBOX_LayerMorph=1`. |

Remember that layer 0 is the **top** and the layer method lives on the **upper** layer.

## 5. Groups and render styles

- Sequence on **groups** for big, coordinated moves. Use individual models and submodels for detail.
- `Per Preview` on a group treats the whole yard as one canvas. Use it for sweeps, waves, and Pictures.
- `Per Model ...` styles give each member its own copy. Use them for "all arches do the same thing".
- `Horizontal/Vertical Per Model` lines the models up in a row. A Bars effect then hops prop to prop.
- An effect on a group and another on a member model at the same time both write the same pixels. Rows
  render in sequencer order, and with model blending (`ModelBlending="true"`, the default) a row
  generally blends over what rows above it already produced on shared pixels. Check the result in the
  preview, and avoid unintentional double-ups.

## 6. Workflow tips

- Rough in the whole song with broad strokes (sections × groups) before detailing. It keeps the energy
  arc coherent.
- Use timing-track snapping. Effects that start a frame late look sloppy.
- Render and watch in the house preview often. Watch at least once at full speed with audio.
- Name layers (`layerName`) for complex rows ("base", "accents").
- Save palettes (`palettes/*.xpalette`) and effect presets so the show feels cohesive across songs.
- Lock (protect) finished effects you don't want to bump.
- Keep a **testing sequence** with a slow chase and RGB/white on each model to verify wiring and colour
  order before sequencing.

## 7. Technical gotchas

- **Frame time**: 50 ms is fine for most shows. Use 25 ms for smooth fast motion on dense pixels.
  Changing it later re-snaps effect times.
- **Audio length**: set `sequenceDuration` to the audio length. Effects past the end are wasted.
- **Model names** must match the layout exactly. Renaming models? Add `oldname:` aliases.
- **Colour order**: if red shows as green, fix the controller or model colour order, not the sequence.
- **Power**: full-white whole-house moments can exceed power injection limits or brown out controllers.
  Use brightness or a white that isn't full RGB.
- **Strobe and seizure safety**: avoid long high-rate strobing (roughly 3+ flashes per second for extended
  periods). Neighbours and drivers see this.
- **Render after edits.** The `.fseq` is what plays. Upload to FPP after re-rendering.
- **Vendor sequences** are built for the vendor's layout. Use xLights's sequence import with model
  mapping rather than renaming your models.

## 8. Generating a sequence as an agent: a recipe

1. Read the layout (`xsq.py layout`). Ask which song, the duration (or read it from the audio), the mood,
   and which props matter most. Ask whether timing tracks already exist.
2. Build the timing: beats, bars, structure (and lyrics if there are faces).
3. Lay a **base layer** per section on the main groups (washes, slow movement, section palette).
4. Add **feature effects** on hero props per section (chorus: tree spirals, matrix pictures; verse:
   faces singing; bridge: something new).
5. Add **accents** on beats or hits (short On/Shockwave/Strobe) on top layers, sparingly.
6. Add fades at section boundaries. Apply brightness value curves for builds.
7. Validate, render headless if possible, then tell the user exactly what you created (sections, props,
   palettes) and what to review in xLights (phoneme timing, beat alignment, brightness).

Generated sequences are a starting point. Encourage the user to watch and tweak, since taste matters more
than rules.
