# Fire effect

XML: `<Effect name="Fire" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Fire_Height` | int | 50 | 1 .. 100 | [VC: `E_VALUECURVE_Fire_Height`] Controls how tall the flames reach. Higher values produce taller flames that extend further across the buffer. |
| `E_SLIDER_Fire_HueShift` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Fire_HueShift`] Shifts the fire color palette hue. At zero the fire is red/yellow; increasing values shift toward other colors like blue or green. |
| `E_TEXTCTRL_Fire_GrowthCycles` | float | 0.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [VC: `E_VALUECURVE_Fire_GrowthCycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of times the fire height oscillates (grows and shrinks) over the effect duration. Zero means no oscillation. |
| `E_CHECKBOX_Fire_GrowWithMusic` | bool | 0 |  | When enabled, flame height is driven by audio volume instead of the Height and Growth Cycles settings. |
| `E_CHOICE_Fire_Location` | enum | Bottom | Bottom, Top, Left, Right | Which edge of the buffer the fire originates from. |
| `E_CHOICE_Fire_Style` | enum | New Render Method | Old Render Method, New Render Method | Selects the rendering algorithm. Old Render Method rebuilds the whole flame every frame, so it flickers in place. New Render Method carries the flame from frame to frame so it rises and drifts like real fire, and renders far faster because the whole grid updates at once (on the GPU where available). |

## Visibility rules (which settings matter when)

- when `Fire_GrowWithMusic == True`: disable Fire_Height, Fire_GrowthCycles
