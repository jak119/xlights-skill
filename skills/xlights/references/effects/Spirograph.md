# Spirograph effect

Note: r should be <= R

XML: `<Effect name="Spirograph" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_Spirograph_Speed` | int | 10 | 0 .. 50 | [VC: `E_VALUECURVE_Spirograph_Speed`] Controls how fast the spirograph pattern rotates over time. Higher values make the drawing point orbit more quickly. |
| `E_SLIDER_Spirograph_R` | int | 20 | 1 .. 100 | [VC: `E_VALUECURVE_Spirograph_R`] Radius of the fixed outer circle as a percentage of the buffer width. This sets the overall size of the spirograph pattern. |
| `E_SLIDER_Spirograph_r` | int | 10 | 1 .. 100 | [VC: `E_VALUECURVE_Spirograph_r`] Radius of the rolling inner circle as a percentage of the buffer width. The ratio of R to r determines the number of lobes in the pattern. Must be less than or equal to R. |
| `E_SLIDER_Spirograph_d` | int | 30 | 1 .. 100 | [VC: `E_VALUECURVE_Spirograph_d`] Distance of the drawing point from the center of the inner circle as a percentage of the buffer width. Controls how far the lobes extend outward. |
| `E_TEXTCTRL_Spirograph_Animate` | int | 0 | -50 .. 50 | [VC: `E_VALUECURVE_Spirograph_Animate`] Gradually changes the distance parameter (d) over time, causing the spirograph pattern to morph and evolve as it draws. |
| `E_TEXTCTRL_Spirograph_Length` | int | 20 | 0 .. 50 | [VC: `E_VALUECURVE_Spirograph_Length`] How much of the spirograph curve is drawn each frame, measured in degrees. Higher values draw more of the pattern, creating a longer visible trail. |
| `E_TEXTCTRL_Spirograph_Width` | int | 1 | 1 .. 50 | [VC: `E_VALUECURVE_Spirograph_Width`] Thickness of the drawn spirograph line in pixels. The line is drawn along the normal to the curve at each point. |
