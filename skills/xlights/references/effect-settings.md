# Effect settings: keys, palettes, value curves, blending, buffers

Per-effect key tables are in `effects/<Name>.md` (generated from xLights's own panel metadata) and
`data/effects.json`. Quick lookup: `python3 scripts/xsq.py effect Bars`.

## Key anatomy

`<PANEL>_<CONTROL>_<Id>`, e.g. `E_SLIDER_Bars_BarCount`.

| Panel prefix | Panel | Stored in |
|---|---|---|
| `E_` | Effect settings (per effect type) | `<EffectDB>` |
| `T_` | Layer Blending / transitions ("Timing" panel historically) | `<EffectDB>` |
| `B_` | Layer Settings / buffer (render style, roto-zoom, blur, sub-buffer) | `<EffectDB>` |
| `C_` | Colour panel (palette, brightness, sparkles, HSV) | `<ColorPalettes>` |

| Control | Value format |
|---|---|
| `SLIDER` | integer, or for float properties with `settingPrefix: SLIDER`, a raw int = value × divisor (e.g. `B_SLIDER_Zoom=10` means 1.0×) |
| `TEXTCTRL` | text; float properties are formatted floats (`E_TEXTCTRL_Bars_Cycles=1.0`, `T_TEXTCTRL_Fadein=0.50`) |
| `CHECKBOX` | `0` / `1` |
| `CHOICE` | option text exactly as listed (case matters: Bars uses `up`, `down`, `Left`, `Right`) |
| `NOTEBOOK` | selected tab label, e.g. `E_NOTEBOOK_SSEFFECT_TYPE=Chase` |
| `SPINCTRL` | integer |
| `FILEPICKERCTRL`, `FONTPICKER`, `COLOURPICKERCTRL` | path / font description / `#rrggbb` |
| `VALUECURVE` | value-curve string (below); overrides the matching slider/text value |

Missing keys fall back to the effect's internal default. Still, write the full default set like xLights
does (`xsq.py` does this for you) so the file reads the same as a hand-made one and survives future
default changes.

## Colour palette (`C_` keys)

```
C_BUTTON_Palette1..8=#rrggbb        8 colour slots (or a colour-curve string, below)
C_CHECKBOX_Palette1..8=0|1          which slots the effect uses
C_SLIDER_Brightness=100             0-400 %, value-curve capable
C_SLIDER_Contrast=0                 -100..100
C_SLIDER_SparkleFrequency=0         0 = off; sparkles overlay
C_CHECKBOX_MusicSparkles=0          sparkles follow music
C_COLOURPICKERCTRL_SparklesColour=#FFFFFF
C_CHECKBOXBRIGHTNESSLEVEL=0         (no underscore after CHECKBOX)
C_SLIDER_Color_HueAdjust / _SaturationAdjust / _ValueAdjust = -100..100
C_CHECKBOX_Chroma, C_SLIDER_ChromaSensitivity, C_COLOURPICKERCTRL_ChromaColour   chroma key
```

Only **enabled** slots are used. How an effect uses them varies:
- Bars, Color Wash, Spirals, Butterfly: cycle through all enabled colours.
- On, Twinkle, Meteors, Fire, Shimmer: mostly first colour or a random pick per element.
- Effects with their own colour choice (SingleStrand `E_CHOICE_SingleStrand_Colors=Rainbow`, Fire
  `Hue shift`, Galaxy, etc.) can ignore the palette.

Hex case doesn't matter. Black in a palette is often used intentionally as "gap" colour for Bars/Spirals.

### Colour curve (gradient over time or space in one slot)

`C_BUTTON_Palette1=Active=TRUE|Id=ID_BUTTON_Palette1|Values=x=0.000^c=#FF0000;x=1.000^c=#0000FF|`
- Optional `Type=` (default Gradient) and `Timecurve=` (0 = over time; others map across the buffer).
- Colours with commas use `@` instead (`rgb(255@ 128@ 0)`). Easiest to create in the UI.

## Value curves (animate a numeric setting over the effect)

Key: the property's `VALUECURVE` key, e.g. `E_VALUECURVE_Bars_Cycles`, `B_VALUECURVE_Rotation`,
`C_VALUECURVE_Brightness`, `T_VALUECURVE_In_Transition_Adjust`. Only properties marked `[VC]` support it.

```
E_VALUECURVE_Bars_Cycles=Active=TRUE|Id=ID_VALUECURVE_Bars_Cycles|Type=Ramp|Min=0.00|Max=300.00|P1=10.00|P2=50.00|RV=TRUE|
```

- `Id=ID_VALUECURVE_<property id>`.
- `Min`/`Max` = the property's slider range in **raw units** (`vcMin`/`vcMax` if given, else `min`/`max` in
  `effects.json`). For divisor properties the raw range is ×divisor (Bars_Cycles 0..300 means 0.0..30.0).
- `RV=TRUE` means P values are real raw values within Min..Max (always write it). Without `RV`, P values are
  0-100 percentages (legacy `.xvc` files).
- Output = curve value ÷ divisor. Above, the ramp runs 10→50 raw, which is 1.0→5.0 cycles.
- Generate with `python3 scripts/xsq.py vc Bars Bars_Cycles Ramp 10 50`.

| Type | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| `Flat` (omit Type=) | level | | | |
| `Ramp` | start | end | | |
| `Ramp Up/Down` | start | mid | end | |
| `Ramp Up/Down Hold` | start/end | mid | mid time % | |
| `Saw Tooth` | start | end | cycles | |
| `Square` | low | high | cycles | |
| `Sine`, `Abs Sine` | start % | amplitude | cycles | vertical offset |
| `Decaying Sine` | start | amplitude | cycles | vertical offset |
| `Parabolic Up/Down`, `Logarithmic Up/Down`, `Exponential Up/Down` | slope/rate | vertical offset | start level | end level |
| `Random` | min | max | points | |
| `Music`, `Inverted Music` | low | high | gain | |
| `Music Trigger Fade` | low | high | trigger | fade |
| `Timing Track Toggle` | low | high | | (needs `TT=<timing track>`) |
| `Timing Track Fade Fixed` / `... Proportional` | low | high | frames / proportion | (needs `TT=`) |
| `Custom` | | | | `Values=x:y;x:y;...` (x 0-1, y 0-1) |

Extra fields: `TT=<timing track>`, `AT=<alt audio track>`, `FT=<label filter>`, `FLR=Y` (regex),
`TO=<time offset>`, `WRAP=TRUE`, `SE=Y` (start/end levels). Keep the plain slider/text key too. The curve
takes precedence while `Active=TRUE`.

## Layer blending (`T_` keys)

Layers render **bottom-up**: the last `<EffectLayer>` is the bottom, `layer 0` is the top. At each pixel,
each upper layer's `T_CHOICE_LayerMethod` combines **this layer ("Effect 1")** with the **composite of all
active layers below ("Effect 2")**. The bottom-most active layer's method is ignored.

| Method | Use it for |
|---|---|
| `Normal` (default) | Alpha-over: this layer covers the ones below except where it's black/transparent. |
| `Effect 1` / `Effect 2` | Show only this layer / only below; with `T_SLIDER_EffectLayerMix` it's a cross-fade. |
| `1 is Mask` | Where this layer is lit, the result goes **dark** (cut-outs). |
| `2 is Mask` | Show this layer only where the layers below are dark. |
| `1 is Unmask` / `1 is True Unmask` | Show the layers below only where this layer is lit (brightness or true colour). Great with Text/Pictures/Shape on top of a wash. |
| `1 reveals 2` | This layer wins wherever it's lit; the layers below show elsewhere (like Normal, ignoring alpha). |
| `2 reveals 1` | The layers below win wherever they're lit; this layer shows only in their dark areas. |
| `Layered` | Same idea as `2 reveals 1`: this layer only fills pixels where the layers below are dark. |
| `Highlight` | This layer shows **only on top of lit pixels below** (a coloured overlay on the shape below). |
| `Highlight Vibrant` | Adds this layer onto the lit pixels below. |
| `Shadow 1 on 2` / `Shadow 2 on 1` | Shifts the hue of one side using the other's brightness (subtle tinting). |
| `Additive` / `Subtractive` | Adds this layer's RGB / subtracts it from the layers below. |
| `Average`, `Max`, `Min`, `Brightness` | Arithmetic mixes. `Max` is a safe "both visible" choice. |
| `Bottom-Top` / `Left-Right` | Split: this layer shows in the bottom / left half, the layers below in the other half. |

Related keys: `T_SLIDER_EffectLayerMix` (0-100), `T_CHECKBOX_LayerMorph` (cross-fade 1→2 over time),
`T_CHECKBOX_Canvas` (this effect sees the pixels below it; **required** for `Warp`, `Kaleidoscope`, and
useful for `Adjust`/`Duplicate`), `T_LayersSelected`.

## Transitions (fade in/out)

```
T_CHOICE_In_Transition_Type=Fade      T_TEXTCTRL_Fadein=0.50     (seconds)
T_CHOICE_Out_Transition_Type=Wipe     T_TEXTCTRL_Fadeout=1.00
T_SLIDER_In_Transition_Adjust=50  T_CHECKBOX_In_Transition_Reverse=0  T_SLIDER_In_Transition_Blur=0
(Out_ equivalents)
```

Types: `Fade`, `Wipe`, `Clock`, `From Middle`, `Square Explode`, `Circle Explode`, `Blinds`, `Blend`,
`Slide Checks`, `Slide Bars`, `Fold`, `Dissolve`, `Circular Swirl`, `Bow Tie`, `Zoom`, `Doorway`, `Blobs`,
`Pinwheel`, `Star`, `Swap`, `Shatter`, `Circles`. A transition only applies when its time is > 0.

Other timing controls: `T_SPINCTRL_SuppressEffectUntil` (frames), `T_SPINCTRL_FreezeEffectAtFrame`.

## Buffer / Layer Settings (`B_` keys)

| Key | Notes |
|---|---|
| `B_CHOICE_BufferStyle` | How the model is unrolled into a 2D canvas. Models: `Default`, `Per Preview`, `Single Line`, `As Pixel` (+ type-specific ones, e.g. trees/stars/arches add more). Groups: `Default`, `Per Preview`, `Horizontal Per Model`, `Vertical Per Model`, `Horizontal Per Model/Strand`, `Vertical Per Model/Strand`, `Horizontal Stack`, `Vertical Stack`, `... - Scaled`, `Single Line`, `Overlay - Centered`, `Overlay - Scaled`, `Single Line Model As A Pixel`, `Default Model As A Pixel`, `Per Model Default`, `Per Model Per Preview`, `Per Model Single Line`, `Per Model Default Deep`, `Per Model Vertical Per Strand`, `Per Model Horizontal Per Strand`. |
| `B_CHOICE_BufferTransform` | `None`, `Rotate CC 90`, `Rotate CW 90`, `Rotate 180`, `Flip Vertical`, `Flip Horizontal`, `Rotate CC 90 Flip Horizontal`, `Rotate CW 90 Flip Horizontal` |
| `B_SLIDER_Blur` | 1-15 (1 = none), VC |
| `B_CUSTOM_SubBuffer` | Restrict the effect to part of the model. Best set in the UI. |
| `B_SLIDER_Rotation` (0-100 = fraction of a turn), `B_SLIDER_Rotations` (×10), `B_SLIDER_Zoom` (×10, 10 = 1.0×), `B_SLIDER_PivotPointX/Y`, `B_SLIDER_XRotation`, `B_SLIDER_YRotation`, `B_SLIDER_ZoomQuality`, `B_CHOICE_RZ_RotationOrder` | Roto-zoom; all VC-capable. |
| `B_CHECKBOX_OverlayBkg` | Overlay background. |
| `B_SPINCTRL_BufferStagger` | Stagger for Stack styles on groups. |
| `B_CHOICE_PerPreviewCamera` | Camera for Per Preview styles (`2D` or a named viewpoint). |

**Per Preview** on a group renders across the models as they're laid out in the house preview. Use it to
sweep an effect across the whole yard. **Per Model** styles render the effect separately on each member,
so every arch does its own thing.

## Dynamic options

Some CHOICE keys take values from the show, not a fixed list:
- `timingTracks` / `lyricTimingTracks`: the name of a timing track in this sequence
  (`E_CHOICE_SingleStrand_TimingTrack`, `E_CHOICE_Faces_TimingTrack`, `E_CHOICE_State_TimingTrack`,
  `E_CHOICE_Shape_FireTimingTrack`, `E_CHOICE_Ripple_TimingTrack`, `E_CHOICE_Text_LyricTrack`...).
- `faces` / `states`: face or state definition names on the target model (`faceInfo`/`stateInfo`).
- `audioTracks`, `xlFonts`, and `effect` (populated by the effect, e.g. SingleStrand FX names).
