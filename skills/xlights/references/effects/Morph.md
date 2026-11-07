# Morph effect

XML: `<Effect name="Morph" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_Morph` = one of 'Start', 'End', 'Options' (default 'Start').
  - Start: `E_SLIDER_Morph_Start_X1`, `E_SLIDER_Morph_Start_Y1`, `E_SLIDER_Morph_Start_X2`, `E_SLIDER_Morph_Start_Y2`, `E_SLIDER_MorphStartLength`, `E_CHECKBOX_Morph_Start_Link`
  - End: `E_SLIDER_Morph_End_X1`, `E_SLIDER_Morph_End_Y1`, `E_SLIDER_Morph_End_X2`, `E_SLIDER_Morph_End_Y2`, `E_SLIDER_MorphEndLength`, `E_CHECKBOX_Morph_End_Link`
  - Options: `E_SLIDER_MorphDuration`, `E_SLIDER_MorphAccel`, `E_SLIDER_Morph_Repeat_Count`, `E_SLIDER_Morph_Repeat_Skip`, `E_SLIDER_Morph_Stagger`, `E_CHECKBOX_ShowHeadAtStart`, `E_CHECKBOX_Morph_AutoRepeat`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Morph_Start_X1` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_Start_X1`] X coordinate of the first endpoint of the starting line (side A start). Defines where the morph begins on one side. |
| `E_SLIDER_Morph_Start_Y1` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_Start_Y1`] Y coordinate of the first endpoint of the starting line (side A start). Defines where the morph begins on one side. |
| `E_SLIDER_Morph_Start_X2` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_Start_X2`] X coordinate of the second endpoint of the starting line (side B start). Together with X1a/Y1a, defines the width and angle of the starting line. |
| `E_SLIDER_Morph_Start_Y2` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_Start_Y2`] Y coordinate of the second endpoint of the starting line (side B start). Together with X1b, defines the other end of the starting line. |
| `E_SLIDER_MorphStartLength` | int | 1 | 0 .. 100 | [VC: `E_VALUECURVE_MorphStartLength`] Length of the colored head at the start of the morph. This value blends with the end head length as the morph progresses. |
| `E_CHECKBOX_Morph_Start_Link` | bool | 0 |  | When enabled, the second start point (X1b/Y1b) is locked to the first start point (X1a/Y1a), making the start a single point instead of a line. |
| `E_SLIDER_Morph_End_X1` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_End_X1`] X coordinate of the first endpoint of the ending line (side A end). Defines where the morph finishes on one side. |
| `E_SLIDER_Morph_End_Y1` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_End_Y1`] Y coordinate of the first endpoint of the ending line (side A end). Defines where the morph finishes on one side. |
| `E_SLIDER_Morph_End_X2` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_End_X2`] X coordinate of the second endpoint of the ending line (side B end). Together with X2a/Y2a, defines the width and angle of the ending line. |
| `E_SLIDER_Morph_End_Y2` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Morph_End_Y2`] Y coordinate of the second endpoint of the ending line (side B end). Together with X2b, defines the other end of the ending line. |
| `E_SLIDER_MorphEndLength` | int | 1 | 0 .. 100 | [VC: `E_VALUECURVE_MorphEndLength`] Length of the colored head at the end of the morph. The head length transitions from the start value to this value as the morph progresses. |
| `E_CHECKBOX_Morph_End_Link` | bool | 0 |  | When enabled, the second end point (X2b/Y2b) is locked to the first end point (X2a/Y2a), making the end a single point instead of a line. |
| `E_SLIDER_MorphDuration` | int | 20 | 0 .. 100 | [VC: `E_VALUECURVE_MorphDuration`] Percentage of the effect duration during which the head is visible and moving. The remaining time shows only the fading tail. |
| `E_SLIDER_MorphAccel` | int | 0 | -10 .. 10 | [VC: `E_VALUECURVE_MorphAccel`] Applies acceleration or deceleration to the morph movement. Positive values speed up toward the end, negative values slow down. |
| `E_SLIDER_Morph_Repeat_Count` | int | 0 | 0 .. 250 | [VC: `E_VALUECURVE_Morph_Repeat_Count`] Number of parallel copies of the morph drawn alongside the original. Creates multiple evenly-spaced morph lines across the model. |
| `E_SLIDER_Morph_Repeat_Skip` | int | 1 | 1 .. 100 | [VC: `E_VALUECURVE_Morph_Repeat_Skip`] Pixel spacing between each repeated morph copy. Higher values spread the repeated morphs farther apart. |
| `E_SLIDER_Morph_Stagger` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Morph_Stagger`] Time offset between repeated morph copies so they start at different times, creating a wave or cascade effect. Negative values reverse the stagger order. |
| `E_CHECKBOX_ShowHeadAtStart` | bool | 0 |  | When enabled, the full head is visible at the starting position from the first frame, rather than growing in from nothing. |
| `E_CHECKBOX_Morph_AutoRepeat` | bool | 0 |  | Automatically calculates the repeat count needed to fill the entire model based on the morph size and skip spacing. |

## Custom controls (set these in the xLights UI if possible)

- `Morph_QuickSet`: Preset start/end point configurations (Full or Single Sweep in each direction) that write predefined values into all eight X/Y coordinate fields at once. Selection resets to blank after the preset is applied.
- `Morph_Swap`: Swap the start and end X/Y coordinate values (and any active value curves) so the morph plays in reverse.

## Visibility rules (which settings matter when)

- when `Morph_Start_Link == True`: disable Morph_Start_X2, Morph_Start_Y2
- when `Morph_End_Link == True`: disable Morph_End_X2, Morph_End_Y2
