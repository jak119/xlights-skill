# Fill effect

XML: `<Effect name="Fill" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Fill_Position` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Fill_Position`] How far the fill extends across the buffer as a percentage. Typically animated with a value curve to create a filling or emptying motion. |
| `E_SLIDER_Fill_Band_Size` | int | 0 | 0 .. 250 | [VC: `E_VALUECURVE_Fill_Band_Size`] Width of each colored band in pixels. When zero, colors blend smoothly across the fill area. |
| `E_SLIDER_Fill_Skip_Size` | int | 0 | 0 .. 250 | [VC: `E_VALUECURVE_Fill_Skip_Size`] Number of blank (black) pixels between each colored band. Only applies when Band Size is greater than zero. |
| `E_SLIDER_Fill_Offset` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Fill_Offset`] Shifts the starting position of the fill. Interpretation depends on the Offset in Pixels setting. |
| `E_CHECKBOX_Fill_Offset_In_Pixels` | bool | 1 |  | When enabled, the offset value is in pixels. When disabled, it is a percentage of the buffer dimension. |
| `E_CHECKBOX_Fill_Color_Time` | bool | 0 |  | When enabled, color is determined by the effect time position. When disabled, color is based on spatial position within the fill. |
| `E_CHECKBOX_Fill_Wrap` | bool | 1 |  | When enabled, the fill wraps around to the beginning of the buffer after reaching the end. |
| `E_CHOICE_Fill_Direction` | enum | Up | Up, Down, Left, Right | Direction the fill progresses across the buffer. |
