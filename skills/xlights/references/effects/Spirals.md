# Spirals effect

XML: `<Effect name="Spirals" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Spirals_Count` | int | 1 | 1 .. 5 | [VC: `E_VALUECURVE_Spirals_Count`] Number of times the full color palette is repeated across the spirals. Higher values create more spiral arms by duplicating the palette pattern. |
| `E_SLIDER_Spirals_Rotation` | float | 20 | -30 .. 30 (raw -300 .. 300, divisor 10) | [VC: `E_VALUECURVE_Spirals_Rotation`] [raw int = value x 10 (e.g. 1.0 -> 10)] Number of times each spiral arm wraps around the model from bottom to top. Negative values reverse the wrap direction. Larger absolute values produce tighter spirals. |
| `E_SLIDER_Spirals_Thickness` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Spirals_Thickness`] Width of each spiral arm as a percentage of the available space. At 100% the arms fill the entire model with no gaps between them. |
| `E_TEXTCTRL_Spirals_Movement` | float | 1.0 | -20 .. 20 (raw -200 .. 200, divisor 10) | [VC: `E_VALUECURVE_Spirals_Movement`] [float text with 1 decimal(s) (e.g. 1.0)] Speed and direction of the spiral rotation. Positive values rotate in one direction, negative in the other. Zero keeps the spirals stationary. |
| `E_CHECKBOX_Spirals_Blend` | bool | 0 |  | When enabled, blends all palette colors vertically across each spiral arm instead of using distinct per-arm colors. |
| `E_CHECKBOX_Spirals_3D` | bool | 0 |  | When enabled, applies a brightness gradient across each spiral arm to simulate a 3D shading effect, making the arms appear rounded. |
| `E_CHECKBOX_Spirals_Grow` | bool | 0 |  | When enabled, the spiral arms gradually increase in thickness over the effect duration. |
| `E_CHECKBOX_Spirals_Shrink` | bool | 0 |  | When enabled, the spiral arms gradually decrease in thickness over the effect duration. When both Grow and Shrink are enabled, the arms grow then shrink. |
