# Galaxy effect

XML: `<Effect name="Galaxy" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_Galaxy` = one of 'Start', 'End', 'Options' (default 'Start').
  - Start: `E_SLIDER_Galaxy_CenterX`, `E_SLIDER_Galaxy_CenterY`, `E_SLIDER_Galaxy_Start_Radius`, `E_SLIDER_Galaxy_Start_Width`, `E_SLIDER_Galaxy_Start_Angle`
  - End: `E_SLIDER_Galaxy_End_Radius`, `E_SLIDER_Galaxy_End_Width`, `E_SLIDER_Galaxy_Revolutions`
  - Options: `E_SLIDER_Galaxy_Duration`, `E_SLIDER_Galaxy_Accel`, `E_CHECKBOX_Galaxy_Reverse`, `E_CHECKBOX_Galaxy_Blend_Edges`, `E_CHECKBOX_Galaxy_Inward`, `E_CHECKBOX_Galaxy_Scale`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Galaxy_CenterX` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Galaxy_CenterX`] Horizontal position of the galaxy center as a percentage of the buffer width. |
| `E_SLIDER_Galaxy_CenterY` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Galaxy_CenterY`] Vertical position of the galaxy center as a percentage of the buffer height. |
| `E_SLIDER_Galaxy_Start_Radius` | int | 1 | 0 .. 250 | [VC: `E_VALUECURVE_Galaxy_Start_Radius`] Inner radius of the spiral arm at the center of the galaxy. |
| `E_SLIDER_Galaxy_Start_Width` | int | 5 | 0 .. 255 | [VC: `E_VALUECURVE_Galaxy_Start_Width`] Thickness of the spiral arm at the inner starting point. |
| `E_SLIDER_Galaxy_Start_Angle` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Galaxy_Start_Angle`] Initial rotation angle of the spiral arm in degrees. |
| `E_SLIDER_Galaxy_End_Radius` | int | 10 | 0 .. 250 | [VC: `E_VALUECURVE_Galaxy_End_Radius`] Outer radius of the spiral arm at the edge of the galaxy. |
| `E_SLIDER_Galaxy_End_Width` | int | 5 | 0 .. 255 | [VC: `E_VALUECURVE_Galaxy_End_Width`] Thickness of the spiral arm at the outer ending point. |
| `E_SLIDER_Galaxy_Revolutions` | float | 1440 | 0 .. 10 (raw 0 .. 3600, divisor 360) | [VC: `E_VALUECURVE_Galaxy_Revolutions`] [raw int = value x 360 (e.g. 1.0 -> 360)] Number of full revolutions the spiral arm wraps around the center. More revolutions create a tighter spiral. settingPrefix:SLIDER because GalaxyEffect::Render calls GetValueCurveInt which reads SLIDER_<id> as a raw pre-divisor int and divides inside ValueCurve. |
| `E_SLIDER_Galaxy_Duration` | int | 20 | 0 .. 100 | [VC: `E_VALUECURVE_Galaxy_Duration`] Percentage of the effect time that the leading head of the spiral is visible. Controls how quickly the spiral appears and disappears. |
| `E_SLIDER_Galaxy_Accel` | int | 0 | -10 .. 10 | [VC: `E_VALUECURVE_Galaxy_Accel`] Adjusts the animation speed curve. Positive values accelerate toward the end, negative values decelerate. |
| `E_CHECKBOX_Galaxy_Reverse` | bool | 0 |  | Reverses the direction the spiral arm rotates. |
| `E_CHECKBOX_Galaxy_Blend_Edges` | bool | 1 |  | When enabled, the spiral arm edges fade smoothly using alpha blending instead of having hard edges. |
| `E_CHECKBOX_Galaxy_Inward` | bool | 0 |  | When enabled, the spiral draws from the outside inward. When disabled, it draws from the center outward. |
| `E_CHECKBOX_Galaxy_Scale` | bool | 1 |  | When enabled, radius and width values are treated as percentages of the buffer size rather than absolute pixel values. |
