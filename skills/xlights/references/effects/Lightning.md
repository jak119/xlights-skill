# Lightning effect

XML: `<Effect name="Lightning" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Number_Bolts` | int | 10 | 1 .. 50 | [VC: `E_VALUECURVE_Number_Bolts`] Number of zigzag segments that make up the lightning bolt. More segments create a longer, more detailed bolt. |
| `E_SLIDER_Number_Segments` | int | 5 | 1 .. 20 | [VC: `E_VALUECURVE_Number_Segments`] Controls the horizontal deviation of each zigzag segment. Higher values make the bolt spread wider side-to-side. |
| `E_CHECKBOX_ForkedLightning` | bool | 0 |  | When enabled, the bolt splits into a secondary fork partway through, creating a branching lightning appearance. |
| `E_SLIDER_Lightning_TopX` | int | 0 | -50 .. 50 | [VC: `E_VALUECURVE_Lightning_TopX`] Horizontal offset of the bolt's starting point relative to center. Negative values shift left, positive shift right. |
| `E_SLIDER_Lightning_TopY` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Lightning_TopY`] Vertical offset of the bolt's starting point. For 'Up' direction this is from the bottom; for 'Down' it offsets from the top. |
| `E_SLIDER_Lightning_BOTX` | int | 0 | -50 .. 50 | Causes the entire bolt to drift horizontally over time. Positive values move right, negative values move left. |
| `E_SLIDER_Lightning_WIDTH` | int | 1 | 1 .. 7 | Pixel thickness of each bolt segment line. Higher values draw a wider, more visible bolt. |
| `E_CHOICE_Lightning_Direction` | enum | Up | Up, Down | Direction the lightning bolt extends. 'Up' draws from bottom to top, 'Down' draws from top to bottom. |
