# Fan effect

XML: `<Effect name="Fan" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_Fan` = one of 'Position', 'Blades', 'Options' (default 'Position').
  - Position: `E_SLIDER_Fan_CenterX`, `E_SLIDER_Fan_CenterY`, `E_SLIDER_Fan_Start_Radius`, `E_SLIDER_Fan_Start_Angle`, `E_SLIDER_Fan_End_Radius`, `E_SLIDER_Fan_Revolutions`
  - Blades: `E_SLIDER_Fan_Num_Blades`, `E_SLIDER_Fan_Blade_Width`, `E_SLIDER_Fan_Blade_Angle`, `E_SLIDER_Fan_Num_Elements`, `E_SLIDER_Fan_Element_Width`
  - Options: `E_SLIDER_Fan_Duration`, `E_SLIDER_Fan_Accel`, `E_CHECKBOX_Fan_Reverse`, `E_CHECKBOX_Fan_Blend_Edges`, `E_CHECKBOX_Fan_Scale`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Fan_CenterX` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Fan_CenterX`] Horizontal position of the fan center as a percentage of the buffer width. |
| `E_SLIDER_Fan_CenterY` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Fan_CenterY`] Vertical position of the fan center as a percentage of the buffer height. |
| `E_SLIDER_Fan_Start_Radius` | int | 1 | 0 .. 2500 | [VC: `E_VALUECURVE_Fan_Start_Radius`] Inner radius of the fan blades. Pixels closer to the center than this are not drawn. |
| `E_SLIDER_Fan_Start_Angle` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Fan_Start_Angle`] Starting rotation angle of the fan blades in degrees. |
| `E_SLIDER_Fan_End_Radius` | int | 50 | 0 .. 2500 | [VC: `E_VALUECURVE_Fan_End_Radius`] Outer radius of the fan blades. Pixels farther from the center than this are not drawn. |
| `E_SLIDER_Fan_Revolutions` | float | 720 | 0 .. 10 (raw 0 .. 3600, divisor 360) | [VC: `E_VALUECURVE_Fan_Revolutions`] [raw int = value x 360 (e.g. 1.0 -> 360)] Total number of revolutions the fan rotates over the duration of the effect. settingPrefix:SLIDER because FanEffect::Render calls GetValueCurveInt which reads SLIDER_<id> as a raw pre-divisor int and divides inside ValueCurve. |
| `E_SLIDER_Fan_Num_Blades` | int | 3 | 1 .. 16 | [VC: `E_VALUECURVE_Fan_Num_Blades`] Number of blades evenly spaced around the fan. |
| `E_SLIDER_Fan_Blade_Width` | int | 50 | 5 .. 100 | [VC: `E_VALUECURVE_Fan_Blade_Width`] Angular width of each blade as a percentage of the space between blades. Higher values make wider blades with less gap. |
| `E_SLIDER_Fan_Blade_Angle` | int | 90 | -360 .. 360 | [VC: `E_VALUECURVE_Fan_Blade_Angle`] Twist angle applied to each blade based on distance from center, creating curved or spiral blade shapes. |
| `E_SLIDER_Fan_Num_Elements` | int | 1 | 1 .. 4 | [VC: `E_VALUECURVE_Fan_Num_Elements`] Number of colored sub-elements within each blade. Each element uses the next palette color. |
| `E_SLIDER_Fan_Element_Width` | int | 100 | 5 .. 100 | [VC: `E_VALUECURVE_Fan_Element_Width`] Width of each element as a percentage of the available element space. Lower values create gaps between elements. |
| `E_SLIDER_Fan_Duration` | int | 80 | 0 .. 100 | [VC: `E_VALUECURVE_Fan_Duration`] Percentage of the effect time that the blades are fully visible. Lower values cause the blades to grow in and shrink out. |
| `E_SLIDER_Fan_Accel` | int | 0 | -10 .. 10 | [VC: `E_VALUECURVE_Fan_Accel`] Adjusts the rotation speed curve. Positive values accelerate toward the end, negative values decelerate. |
| `E_CHECKBOX_Fan_Reverse` | bool | 0 |  | Reverses the direction of fan rotation. |
| `E_CHECKBOX_Fan_Blend_Edges` | bool | 1 |  | When enabled, blade edges fade smoothly using alpha or brightness instead of having hard edges. |
| `E_CHECKBOX_Fan_Scale` | bool | 1 |  | When enabled, radius values are treated as percentages of the buffer size rather than absolute pixel values. |
