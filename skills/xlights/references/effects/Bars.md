# Bars effect

XML: `<Effect name="Bars" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Bars_BarCount` | int | 1 | 1 .. 5 | [VC: `E_VALUECURVE_Bars_BarCount`] Number of times the full palette color sequence repeats across the model. Higher values produce more, thinner bars. |
| `E_TEXTCTRL_Bars_Cycles` | float | 1.0 | 0 .. 30 (raw 0 .. 300, divisor 10) | [VC: `E_VALUECURVE_Bars_Cycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of times the bars scroll completely across the model during the effect. Higher values make the bars move faster. |
| `E_CHOICE_Bars_Direction` | enum | up | up, down, expand, compress, Left, Right, H-expand, H-compress, Alternate Up, Alternate Down, Alternate Left, Alternate Right, Custom Horz, Custom Vert, Custom | Direction the bars travel. Expand/compress radiate from or collapse toward a center point. Alternate modes snap bars one step at a time. Custom Horz/Vert place static bars with an adjustable center offset. Custom moves the bars at any angle set by the Angle slider. |
| `E_SLIDER_Bars_Angle` | int | 90 | -180 .. 180 | [VC: `E_VALUECURVE_Bars_Angle`] Direction in degrees the bars travel when Direction is Custom. 0 is right, 90 is up, -90 is down, 180 or -180 is left. |
| `E_TEXTCTRL_Bars_Center` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Bars_Center`] Shifts the expansion/compression origin or the static bar offset. 0 is the model center; negative values shift left/down, positive values shift right/up. |
| `E_CHECKBOX_Bars_Highlight` | bool | 0 |  | Adds a bright white highlight line at the leading edge of each bar to make the boundaries between colors more visible. |
| `E_CHECKBOX_Bars_UseFirstColorForHighlight` | bool | 0 |  | When Highlight is enabled, uses the first palette color for the highlight line instead of white. The first color is then excluded from the bar pattern. |
| `E_CHECKBOX_Bars_3D` | bool | 0 |  | Applies a brightness or alpha gradient within each bar so it fades from full brightness at one edge to dark at the other, giving a three-dimensional appearance. |
| `E_CHECKBOX_Bars_Gradient` | bool | 0 |  | Smoothly blends colors between adjacent bars instead of using hard edges, creating a continuous gradient across the palette. |

## Visibility rules (which settings matter when)

- when `Bars_Direction in ['expand', 'compress', 'H-expand', 'H-compress', 'Custom Horz', 'Custom Vert']`: enable Bars_Center
- when `Bars_Direction == 'Custom'`: enable Bars_Angle
