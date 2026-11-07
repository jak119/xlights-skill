# On effect

XML: `<Effect name="On" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_Eff_On_Start` | int | 100 | 0 .. 100 | Sets the brightness level at the beginning of the effect as a percentage of the palette color's full value. |
| `E_TEXTCTRL_Eff_On_End` | int | 100 | 0 .. 100 | Sets the brightness level at the end of the effect as a percentage. The intensity ramps linearly from Start to End over the effect duration. |
| `E_TEXTCTRL_On_Transparency` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_On_Transparency`] Sets the alpha transparency of the effect. At 0 the color is fully opaque; at 100 it is fully transparent, allowing effects on lower layers to show through. |
| `E_TEXTCTRL_On_Cycles` | float | 1.0 | 0 .. 100 (raw 0 .. 1000, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] Number of times the start-to-end intensity ramp repeats over the effect duration. Values greater than 1 create a pulsing look. |
| `E_CHECKBOX_On_Shimmer` | bool | 0 |  | When enabled, the effect alternates between the first and second palette colors on each frame, creating a rapid flickering shimmer. |
