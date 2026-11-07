# Sketch effect

XML: `<Effect name="Sketch" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_SketchBackgroundOpacity` | int | 48 | 0 .. 255 | Opacity (0-255) of the background tracing image when shown inside the Effect Assist panel. Has no effect on rendering — just controls how prominent the reference image is when sketching. |
| `E_SLIDER_DrawPercentage` | int | 40 | 0 .. 100 | [VC: `E_VALUECURVE_DrawPercentage`] Percentage of the effect duration over which the sketch progressively draws on. The remaining duration shows the fully drawn sketch. Disabled when Motion is enabled. |
| `E_SLIDER_Thickness` | int | 1 | 1 .. 25 | [VC: `E_VALUECURVE_Thickness`] Line thickness in pixels used when drawing the sketch. |
| `E_CHECKBOX_MotionEnabled` | bool | 0 |  | When enabled, the sketch is fully drawn over the entire effect duration but only a percentage is rendered at any given time, creating simple motion-graphics-like effects. |
| `E_SLIDER_MotionPercentage` | int | 100 | 1 .. 100 | [VC: `E_VALUECURVE_MotionPercentage`] When Motion is enabled, percentage of the sketch to render at any given time. Only used when Motion is enabled. |

## Custom controls (set these in the xLights UI if possible)

- `Sketch_Info`: Explanatory text describing the Sketch effect plus links to demo videos. Display only — not part of the saved effect.
- `Sketch_DefRow`: Read-only display of the active sketch definition string. The actual sketch is drawn / edited via the Effect Assist panel; this control just shows the resulting definition.
- `Sketch_BackgroundRow`: Background image used as a tracing reference inside the Effect Assist panel. The image itself is not rendered into the effect output.

## Visibility rules (which settings matter when)

- when `MotionEnabled == True`: enable MotionPercentage; disable DrawPercentage
