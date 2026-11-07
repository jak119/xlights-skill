# Animations and ambient shows (no music)

Not every show is synced to a song. Many displays, especially early on, run **animated looks** that loop
all evening: slow colour washes, twinkles, chases, a gentle Halloween flicker. This is a perfectly good
way to run a display, and it's the easiest place to start.

## How an animation differs in the file

- `<sequenceType>Animation</sequenceType>` with an empty `<mediaFile/>`. `xsq.py new` does this
  automatically when you don't pass `--media`.
- You choose `<sequenceDuration>`. Nothing has to line up with audio.
- Timing tracks are optional. A **fixed-interval** track (`add_timing("Grid", fixed=1000)`) is handy for
  snapping effects to round seconds, or to drive "on each mark" effects at a steady tempo.
- Everything else (models, layers, palettes, blending) works exactly the same.

```bash
python3 scripts/xsq.py new "/path/Show/Porch Glow.xsq" --duration 60 --models "Porch,Railing"
```

## Ask the user first

- **Which props, and what feel?** Calm and pretty, festive and busy, spooky, or a mix?
- **How long should one loop be, and will it repeat?** Most ambient sequences are 30 s to 5 min and loop
  in the player.
- **One look or a rotation?** A playlist of 3–6 short looks that cycle feels more alive than one long
  loop.
- **What plays it?** FPP, xSchedule, or a controller's own playback. That decides how looping and
  scheduling are set up (see below).

## Making loops seamless

When a sequence repeats, the last frame jumps straight to the first. Hide the seam:

- **Whole cycles.** Set cycle and rotation counts so the motion ends where it started. For example,
  `E_TEXTCTRL_Bars_Cycles=2.0` rather than `2.3`, and `E_TEXTCTRL_ColorWash_Cycles=1.0`. Pick round numbers
  for Spirals movement, SingleStrand `Chase_Rotations`, and Butterfly/Plasma speeds over the full effect
  length. Check with a render, because some effects' motion isn't a simple cycle count.
- **Effects span the whole loop**, from 0 to the end, on each base layer. Gaps or partial effects show as
  a blink at the loop point.
- **Random textures loop for free.** Twinkle, Shimmer, Snowflakes, Fire, Candle, Meteors, and Lightning
  have no obvious start or end. They're ideal for long ambient loops.
- **Fade through black if needed.** If the start and end really differ, fade out over the last 1–2 s and
  in over the first 1–2 s (`T_TEXTCTRL_Fadein`/`Fadeout`). A brief dip reads as intentional.
- **Avoid one-shot effects** (a single sweep, Shockwave, a Fireworks burst) at the very start or end of a
  loop, unless the "reset" is the point.

## Ambient design tips

- **Slow is calming, fast is exciting.** Ambient looks usually want slow motion: long colour-wash
  cycles, slow chases, gentle twinkle steps. Save fast and strobing looks for short bursts.
- **One base plus one texture is often enough.** A dim Color Wash with a Twinkle layer on top is a
  classic that looks good for hours. The user's own `Halloween_v3` style (twinkle over a slow
  orange/purple wash) is exactly this.
- **Vary over minutes, not seconds.** Change the palette or effect every 15–60 s (or rotate sequences in a
  playlist) so people walking by see something change, without it feeling frantic.
- **Use the whole display gently.** Sweep a slow wave across a group (`Per Preview` buffer), or let props
  take turns being the bright one.
- **Watch brightness and power.** Displays that run for hours at full white are hard on power supplies
  and neighbours. Ambient looks at 30–60% brightness usually look richer anyway.
- **Theme by palette.** The same effects become Christmas, Halloween, Valentine's or Fourth of July just by
  swapping the palette (see `color-and-leds.md`).
- **Avoid long strobing.** Rapid flashing for minutes is unpleasant and can be a seizure risk.

## Starter looks

| Look | Recipe |
|---|---|
| Calm glow | Color Wash, 1 cycle over the loop, 2–3 analogous colours, brightness 40–60 %. |
| Starry | Dim blue/purple Color Wash base + white Twinkle on top (`Normal`). |
| Candy chase | SingleStrand Chase, red/white, `Chase_Rotations` a whole number, 60–120 s loop. |
| Spooky flicker | Fire or Candle in orange, plus occasional purple Lightning or Strobe accents (sparingly). |
| Snowfall | Snowflakes or Meteors (down) in white/ice blue over a dark blue wash. |
| Festive rotate | 4 × 15 s segments on one layer: Bars → Spirals → Twinkle → Color Wash, each fading into the next. |
| Breathing / pulse | `On` with `E_TEXTCTRL_Eff_On_Start=100`, `E_TEXTCTRL_Eff_On_End=20`, `E_TEXTCTRL_On_Cycles=6.0` (repeats the ramp 6 times), or alternate short On effects ramping up then down. For a smooth sine pulse, add a Sine value curve on Brightness in the xLights UI. |

## Playing animations on a loop

- **FPP**: put the `.fseq` in a playlist, set the playlist to repeat, and schedule it nightly (for
  example dusk to 10 pm). Several short sequences in one playlist give a rotating show.
- **xSchedule**: add the sequences to a playlist, enable looping, and set a schedule.
- **Re-render** after every change. The player uses the `.fseq`, not the `.xsq`.

These are the user's player settings. Explain them and let the user set them up, rather than changing
them yourself.

## Growing into music later

Animations are a great way to learn effects, palettes, and layering. When the user is ready for a
musical show, the same props and palettes carry over. See `sequencing-guide.md` and
`timing-and-lyrics.md`.
