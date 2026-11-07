# Moving Head effect

XML: `<Effect name="Moving Head" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK2` = one of 'Color', 'ColorWheel' (default 'Color').
  - ColorWheel: `E_CHECKBOX_AUTO_SHUTTER`
- `E_NOTEBOOK1` = one of 'Position', 'Dimmer', 'Pathing', 'Pattern', 'Control', 'Link', 'Status' (default 'Position').
  - Position: `E_TEXTCTRL_MHPan`, `E_TEXTCTRL_MHTilt`, `E_TEXTCTRL_MHPanOffset`, `E_TEXTCTRL_MHTiltOffset`, `E_SLIDER_MHGroupings`, `E_TEXTCTRL_MHCycles`
  - Pathing: `E_TEXTCTRL_MHPathDef`, `E_TEXTCTRL_MHPathScale`, `E_TEXTCTRL_MHTimeOffset`, `E_CHECKBOX_MHIgnorePan`, `E_CHECKBOX_MHIgnoreTilt`
  - Pattern: `E_CHECKBOX_MHPatternEnable`, `E_CHOICE_MHPattern`, `E_SLIDER_MHPatternWidth`, `E_SLIDER_MHPatternHeight`, `E_SLIDER_MHPatternXOffset`, `E_SLIDER_MHPatternYOffset`, `E_SLIDER_MHPatternRotation`, `E_SLIDER_MHPatternStartOffset`, `E_SLIDER_MHPatternPhaseOffset`, `E_SLIDER_MHPatternXFreq`, `E_SLIDER_MHPatternYFreq`, `E_SLIDER_MHPatternXPhase`, `E_SLIDER_MHPatternYPhase`
  - Control: `E_CHECKBOX_AUTO_SHUTTER`, `E_CHECKBOX_MHShutterEnable`
  - Link: `E_CHECKBOX_MHLinkToNext`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_MHPan` | float | 0.0 | -180 .. 180 (raw -1800 .. 1800, divisor 10) | [VC: `E_VALUECURVE_MHPan`] [float text with 1 decimal(s) (e.g. 1.0)] The horizontal pan angle in degrees for the moving head fixture. Controls left/right beam positioning. |
| `E_TEXTCTRL_MHTilt` | float | 0.0 | -180 .. 180 (raw -1800 .. 1800, divisor 10) | [VC: `E_VALUECURVE_MHTilt`] [float text with 1 decimal(s) (e.g. 1.0)] The vertical tilt angle in degrees for the moving head fixture. Controls up/down beam positioning. |
| `E_TEXTCTRL_MHPanOffset` | float | 0.0 | -180 .. 180 (raw -1800 .. 1800, divisor 10) | [VC: `E_VALUECURVE_MHPanOffset`] [float text with 1 decimal(s) (e.g. 1.0)] Pan offset in degrees applied incrementally across grouped fixtures, fanning them apart horizontally. Creates a spread effect when multiple heads are grouped. |
| `E_TEXTCTRL_MHTiltOffset` | float | 0.0 | -180 .. 180 (raw -1800 .. 1800, divisor 10) | [VC: `E_VALUECURVE_MHTiltOffset`] [float text with 1 decimal(s) (e.g. 1.0)] Tilt offset in degrees applied incrementally across grouped fixtures, fanning them apart vertically. Creates a spread effect when multiple heads are grouped. |
| `E_SLIDER_MHGroupings` | int | 1 | 1 .. 6 | [VC: `E_VALUECURVE_MHGroupings`] Number of fixture groupings for fan offset distribution. Fixtures within the same group share the same pan/tilt, with fan offsets applied between groups. |
| `E_TEXTCTRL_MHCycles` | float | 0.1 | 0 .. 10 (raw 0 .. 100, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] Number of full movement cycles to complete over the effect duration. Controls how many times a pathing animation repeats. |
| `E_TEXTCTRL_MHPathDef` | string |  |  | Encoded definition string for the movement path. Defines waypoints and curves that the moving head beam follows over time. |
| `E_TEXTCTRL_MHPathScale` | float | 0.0 | -10 .. 10 (raw -100 .. 100, divisor 10) | [VC: `E_VALUECURVE_MHPathScale`] [float text with 1 decimal(s) (e.g. 1.0)] Scales the size of the movement path. Positive values enlarge the path, negative values shrink it, and zero uses the default size. |
| `E_TEXTCTRL_MHTimeOffset` | float | 0.0 | -100 .. 100 (raw -1000 .. 1000, divisor 10) | [VC: `E_VALUECURVE_MHTimeOffset`] [float text with 1 decimal(s) (e.g. 1.0)] Shifts the starting point in time along the movement path. Use to stagger multiple fixtures following the same path at different phases. |
| `E_CHECKBOX_MHIgnorePan` | bool | 0 |  | When enabled, the pan component of the path is ignored, keeping the fixture at its current horizontal position while only tilt changes. |
| `E_CHECKBOX_MHIgnoreTilt` | bool | 0 |  | When enabled, the tilt component of the path is ignored, keeping the fixture at its current vertical position while only pan changes. |
| `E_CHECKBOX_AUTO_SHUTTER` | bool | 0 |  | When enabled, the fixture shutter automatically opens when the dimmer is above zero and closes when the dimmer is zero, preventing unwanted light leaks during repositioning. |
| `E_CHECKBOX_MHShutterEnable` | bool | 0 |  | Holds the fixture shutter open at the model's Shutter On value for the whole effect. Auto Shutter still takes over when it is active. |
| `E_CHECKBOX_MHPatternEnable` | bool | 0 |  | Drives Pan/Tilt from a parametric shape generator instead of (or on top of) the waypoint path. |
| `E_CHOICE_MHPattern` | enum | Circle | Circle, Eight, Line, Line2, Diamond, Square, SquareChoppy, SquareTrue, Leaf, Lissajous | Parametric shape the beam traces over the effect duration. Modelled on QLC+ EFX shapes. |
| `E_SLIDER_MHPatternWidth` | int | 90 | 0 .. 180 | Half-width of the pattern in pan degrees. |
| `E_SLIDER_MHPatternHeight` | int | 45 | 0 .. 180 | Half-height of the pattern in tilt degrees. |
| `E_SLIDER_MHPatternXOffset` | int | 0 | -180 .. 180 | Pan-axis centre of the pattern in degrees. |
| `E_SLIDER_MHPatternYOffset` | int | 0 | -180 .. 180 | Tilt-axis centre of the pattern in degrees. |
| `E_SLIDER_MHPatternRotation` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_MHPatternRotation`] Rotates the whole pattern about its centre, in degrees. Animate it with a value curve to spin the shape over the effect. |
| `E_SLIDER_MHPatternStartOffset` | int | 0 | 0 .. 360 | Shifts where along the shape the beam starts, in degrees. |
| `E_SLIDER_MHPatternPhaseOffset` | int | 0 | -360 .. 360 | Staggers grouped fixtures along the shape so they chase each other around it. Only meaningful for a model group. |
| `E_SLIDER_MHPatternXFreq` | int | 2 | 0 .. 32 | Lissajous only: pan-axis frequency multiplier. |
| `E_SLIDER_MHPatternYFreq` | int | 3 | 0 .. 32 | Lissajous only: tilt-axis frequency multiplier. |
| `E_SLIDER_MHPatternXPhase` | int | 90 | 0 .. 360 | Lissajous only: pan-axis phase in degrees. |
| `E_SLIDER_MHPatternYPhase` | int | 0 | 0 .. 360 | Lissajous only: tilt-axis phase in degrees. |
| `E_CHECKBOX_MHLinkToNext` | bool | 0 |  | Snaps every active head's Pan/Tilt to where the next Moving Head effect on this row starts, and forces the Dimmer to 0 so the head moves into position dark. |
| `E_TEXTCTRL_MH1_Settings` | string |  |  | Per-fixture override settings for moving head fixture 1. Stores individual pan, tilt, and other parameters that differ from the group defaults. |
| `E_TEXTCTRL_MH2_Settings` | string |  |  | Per-fixture override settings for moving head fixture 2. |
| `E_TEXTCTRL_MH3_Settings` | string |  |  | Per-fixture override settings for moving head fixture 3. |
| `E_TEXTCTRL_MH4_Settings` | string |  |  | Per-fixture override settings for moving head fixture 4. |
| `E_TEXTCTRL_MH5_Settings` | string |  |  | Per-fixture override settings for moving head fixture 5. |
| `E_TEXTCTRL_MH6_Settings` | string |  |  | Per-fixture override settings for moving head fixture 6. |
| `E_TEXTCTRL_MH7_Settings` | string |  |  | Per-fixture override settings for moving head fixture 7. |
| `E_TEXTCTRL_MH8_Settings` | string |  |  | Per-fixture override settings for moving head fixture 8. |

## Visibility rules (which settings matter when)

- when `MHPatternEnable == True`: enable MHPattern, MHPatternWidth, MHPatternHeight, MHPatternXOffset, MHPatternYOffset, MHPatternRotation, MHPatternStartOffset, MHPatternPhaseOffset, MHPatternXFreq, MHPatternYFreq, MHPatternXPhase, MHPatternYPhase
- when `MHPattern == 'Lissajous'`: enable MHPatternXFreq, MHPatternYFreq, MHPatternXPhase, MHPatternYPhase
