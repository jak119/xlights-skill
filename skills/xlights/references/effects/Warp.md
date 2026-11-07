# Warp effect

The warp effect distorts the pixels in the layers below it. The Canvas option in Layer Blending must be enabled for it to work.

XML: `<Effect name="Warp" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

**Canvas effect**: set `T_CHECKBOX_Canvas=1`; it transforms the layers below it.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Warp_Type` | enum | water drops | water drops, dissolve, circle reveal, banded swirl, ripple, single water drop, circular swirl, drop, wavy, sample on, mirror, copy, flip, speed | The distortion algorithm applied to pixels from lower layers. Options include water drops, dissolve, circle reveal, swirls, ripples, mirroring, copying, and flipping. |
| `E_CHOICE_Warp_Treatment_APPLYLAST` | enum | constant | constant, in, out | Controls how the warp intensity changes over the effect duration. Constant maintains full distortion, In ramps from none to full, and Out ramps from full to none. |
| `E_SLIDER_Warp_X` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Warp_X`] Horizontal position of the warp center point or focal area, as a percentage of the buffer width. |
| `E_SLIDER_Warp_Y` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Warp_Y`] Vertical position of the warp center point or focal area, as a percentage of the buffer height. |
| `E_TEXTCTRL_Warp_Cycle_Count` | int | 1 | 1 .. 10 | Number of times the warp animation repeats over the effect duration. Higher values make the distortion cycle faster. |
| `E_TEXTCTRL_Warp_Speed` | int | 20 | 0 .. 40 | Controls the rate at which the warp distortion animates. Higher values produce faster-moving distortion patterns. |
| `E_TEXTCTRL_Warp_Frequency` | int | 20 | 0 .. 40 | Controls the spatial frequency of the distortion pattern. Higher values create tighter, more closely spaced ripples or waves. |

## Visibility rules (which settings matter when)

- when `Warp_Type not in ['dissolve', 'drop', 'wavy']`: enable Warp_X
- when `Warp_Type not in ['dissolve', 'drop', 'wavy', 'speed']`: enable Warp_Y
- when `Warp_Type not in ['water drops', 'wavy', 'sample on', 'mirror', 'transpose', 'speed'] AND Warp_Treatment_APPLYLAST == 'constant'`: enable Warp_Cycle_Count
- when `Warp_Type in ['water drops', 'ripple', 'circular swirl', 'wavy']`: enable Warp_Speed
- when `Warp_Type in ['banded swirl', 'ripple']`: enable Warp_Frequency
