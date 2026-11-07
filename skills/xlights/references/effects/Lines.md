# Lines effect

XML: `<Effect name="Lines" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Lines_Objects` | int | 2 | 1 .. 20 | Number of independent line objects drawn on the model. Each line uses the next color from the palette. |
| `E_SLIDER_Lines_Segments` | int | 3 | 2 .. 6 | Number of control points per line. Lines are drawn between consecutive points, so more points create multi-segment polylines. |
| `E_SLIDER_Lines_Thickness` | int | 1 | 1 .. 10 | [VC: `E_VALUECURVE_Lines_Thickness`] Pixel width of each drawn line. Higher values produce thicker, bolder lines. |
| `E_TEXTCTRL_Lines_Speed` | float | 1.0 | 0 .. 10 (raw 0 .. 100, divisor 10) | [VC: `E_VALUECURVE_Lines_Speed`] [float text with 1 decimal(s) (e.g. 1.0)] How fast the line points move across the model. Points bounce off the edges when they reach the boundary. |
| `E_SLIDER_Lines_Trails` | int | 0 | 0 .. 10 | Number of trailing afterimages left behind each line, creating a motion trail effect. Zero means no trails. |
| `E_CHECKBOX_Lines_FadeTrails` | bool | 1 |  | When enabled, older trail copies fade out progressively, creating a smooth motion blur. When disabled, all trail copies are drawn at full opacity. |
