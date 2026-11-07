# Wave effect

XML: `<Effect name="Wave" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Wave_Type` | enum | Sine | Sine, Triangle, Square, Decaying Sine, Fractal/ivy | The waveform shape drawn across the model. Sine produces smooth curves, Triangle creates sharp zigzags, Square makes flat-topped waves, Decaying Sine fades over time, and Fractal/ivy generates random branching patterns. |
| `E_CHOICE_Fill_Colors` | enum | None | None, Rainbow, Palette | How the area below the wave is filled. None leaves it empty, Rainbow fills with a hue gradient, and Palette fills using the effect color palette. |
| `E_CHECKBOX_Mirror_Wave` | bool | 0 |  | When enabled, a mirrored copy of the wave is drawn on the opposite side, creating a symmetrical pattern around the center. |
| `E_TEXTCTRL_Number_Waves` | float | 2.50 | 0.5 .. 10 (raw 180 .. 3600, divisor 360) | [VC: `E_VALUECURVE_Number_Waves`] [float text with 2 decimal(s) (e.g. 1.00)] Number of wave cycles drawn across the buffer width. 1.0 is one full wave; fractional values draw partial waves. Higher values fit more wave cycles onto the model. |
| `E_SLIDER_Thickness_Percentage` | int | 5 | 0 .. 100 | [VC: `E_VALUECURVE_Thickness_Percentage`] Vertical thickness of the wave line as a percentage of the buffer height. Higher values draw a wider band around the wave center. |
| `E_SLIDER_Wave_Height` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Wave_Height`] Scales the vertical amplitude of the wave as a percentage. Lower values flatten the wave; higher values make it reach closer to the buffer edges. |
| `E_TEXTCTRL_Wave_Speed` | float | 10.00 | 0 .. 50 (raw 0 .. 5000, divisor 100) | [VC: `E_VALUECURVE_Wave_Speed`] [float text with 2 decimal(s) (e.g. 1.00)] How fast the wave scrolls horizontally across the model. Higher values create faster-moving waves. |
| `E_CHOICE_Wave_Direction` | enum | Right to Left | Right to Left, Left to Right | The horizontal direction the wave scrolls. Right to Left moves the pattern leftward, Left to Right moves it rightward. |
| `E_SLIDER_Wave_YOffset` | int | 0 | -250 .. 250 | [VC: `E_VALUECURVE_Wave_YOffset`] Shifts the wave centerline up or down from the middle of the buffer. Positive values move the wave up, negative values move it down. |

## Visibility rules (which settings matter when)

- when `Wave_Type == 'Fractal/ivy'`: disable Number_Waves
