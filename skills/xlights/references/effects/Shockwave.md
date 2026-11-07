# Shockwave effect

XML: `<Effect name="Shockwave" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_Shockwave` = one of 'Position', 'Options' (default 'Position').
  - Position: `E_SLIDER_Shockwave_CenterX`, `E_SLIDER_Shockwave_CenterY`, `E_SLIDER_Shockwave_Start_Radius`, `E_SLIDER_Shockwave_End_Radius`, `E_SLIDER_Shockwave_Start_Width`, `E_SLIDER_Shockwave_End_Width`
  - Options: `E_SLIDER_Shockwave_Accel`, `E_SLIDER_Shockwave_Cycles`, `E_CHECKBOX_Shockwave_Blend_Edges`, `E_CHECKBOX_Shockwave_Scale`, `E_CHOICE_Shockwave_TimingTrack`, `E_TEXTCTRL_Shockwave_FilterLabel`, `E_CHECKBOX_Shockwave_FilterRegex`, `E_SLIDER_Shockwave_Duration`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Shockwave_CenterX` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Shockwave_CenterX`] Horizontal center of the shockwave ring as a percentage of the buffer width. |
| `E_SLIDER_Shockwave_CenterY` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Shockwave_CenterY`] Vertical center of the shockwave ring as a percentage of the buffer height. |
| `E_SLIDER_Shockwave_Start_Radius` | int | 1 | 0 .. 750 | [VC: `E_VALUECURVE_Shockwave_Start_Radius`] Starting radius of the expanding ring at the beginning of each cycle. |
| `E_SLIDER_Shockwave_End_Radius` | int | 10 | 0 .. 750 | [VC: `E_VALUECURVE_Shockwave_End_Radius`] Ending radius of the expanding ring at the end of each cycle. |
| `E_SLIDER_Shockwave_Start_Width` | int | 5 | 0 .. 255 | [VC: `E_VALUECURVE_Shockwave_Start_Width`] Thickness of the ring band at the start of each cycle. |
| `E_SLIDER_Shockwave_End_Width` | int | 10 | 0 .. 255 | [VC: `E_VALUECURVE_Shockwave_End_Width`] Thickness of the ring band at the end of each cycle. |
| `E_SLIDER_Shockwave_Accel` | int | 0 | -10 .. 10 | Adjusts the expansion speed curve. Positive values make the ring expand slowly then accelerate; negative values make it start fast then decelerate. |
| `E_SLIDER_Shockwave_Cycles` | int | 1 | 1 .. 100 | Number of times the shockwave ring expands from Radius1 to Radius2 over the effect duration. In timing track mode, this many rings fire per timing mark. |
| `E_CHECKBOX_Shockwave_Blend_Edges` | bool | 1 |  | When enabled, the ring edges fade out smoothly based on distance from the ring center, creating a soft glow instead of hard edges. |
| `E_CHECKBOX_Shockwave_Scale` | bool | 1 |  | When enabled, radius and width values are treated as percentages of the buffer size. When disabled, values are in absolute pixels. |
| `E_CHOICE_Shockwave_TimingTrack` | enum |  | (dynamic: timingTracks) | When set, each timing mark triggers a new shockwave ring expansion. Duration controls how long each expansion lasts. |
| `E_TEXTCTRL_Shockwave_FilterLabel` | string |  |  | Text filter applied to timing track labels. Only timing marks whose labels match this filter text will trigger a shockwave. |
| `E_CHECKBOX_Shockwave_FilterRegex` | bool | 0 |  | When enabled, the filter text is treated as a regular expression pattern instead of a plain text match. |
| `E_SLIDER_Shockwave_Duration` | int | 1000 | 50 .. 5000 | How long each shockwave ring expansion lasts in milliseconds after a timing mark fires. Only active when a Timing Track is selected. |

## Visibility rules (which settings matter when)

- when `Shockwave_TimingTrack not in ['']`: enable Shockwave_FilterLabel, Shockwave_FilterRegex, Shockwave_Duration
- when `Shockwave_TimingTrack in ['']`: disable Shockwave_FilterLabel, Shockwave_FilterRegex, Shockwave_Duration
