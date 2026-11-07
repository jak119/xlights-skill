# Ripple effect

XML: `<Effect name="Ripple" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Ripple_Draw_Style` | enum | Old | Old, Lines Inward, Lines Outward, Lines Both, Lines Inward Ripple, Lines Outward Ripple, Lines Both Ripple, Solid Inward, Solid Outward, Solid Both, Solid Inward Ripple, Solid Outward Ripple, Solid Both Ripple, Highlight Inward, Highlight Outward, Highlight Both, Highlight Inward Ripple, Highlight Outward Ripple, Highlight Both Ripple | Rendering style and direction for the ripple waves. Lines draw outlines only, Solid fills the shapes, and Highlight emphasizes edges. Inward/Outward/Both controls the wave direction, and Ripple variants add repeated wave pulses. |
| `E_CHOICE_Ripple_Object_To_Draw` | enum | Circle | Circle, Square, Triangle, Star, Polygon, Heart, Tree, Candy Cane, Snow Flake, Crucifix, Present, SVG | Shape of the ripple waves expanding from the center. Choose from geometric shapes, holiday objects, or load a custom SVG outline. |
| `E_CHOICE_Ripple_Movement` | enum | Explode | Explode, Implode, None | Controls whether ripple waves expand outward (Explode), contract inward (Implode), or remain stationary (None) over the effect duration. |
| `E_SLIDER_Ripple_Scale` | int | 100 | 0 .. 500 | [VC: `E_VALUECURVE_Ripple_Scale`] Overall size of the ripple pattern as a percentage. Values above 100 expand the ripples beyond the model boundaries. |
| `E_TEXTCTRL_Ripple_Outline` | float | 1.0 | 0 .. 10 (raw 0 .. 100, divisor 10) | [VC: `E_VALUECURVE_Ripple_Outline`] [float text with 1 decimal(s) (e.g. 1.0)] Thickness of each ripple line. Higher values draw wider ripple bands; lower values produce thinner outlines. |
| `E_SLIDER_Ripple_Thickness` | int | 3 | 1 .. 100 | [VC: `E_VALUECURVE_Ripple_Thickness`] Number of concentric ripple rings displayed simultaneously. More ripples create a denser wave pattern. |
| `E_TEXTCTRL_Ripple_Spacing` | float | 1.0 | 0.1 .. 40 (raw 1 .. 400, divisor 10) | [VC: `E_VALUECURVE_Ripple_Spacing`] [float text with 1 decimal(s) (e.g. 1.0)] Distance between consecutive ripple rings. Larger values spread the rings farther apart. |
| `E_TEXTCTRL_Ripple_Cycles` | float | 1.0 | 0 .. 30 (raw 0 .. 300, divisor 10) | [VC: `E_VALUECURVE_Ripple_Cycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of complete ripple animation cycles over the effect duration. Higher values repeat the expand/contract motion more times. |
| `E_SLIDER_RIPPLE_POINTS` | int | 5 | 3 .. 8 | Number of points for star, polygon, and snowflake shapes. Only applies when one of those shapes is selected. |
| `E_SLIDER_Ripple_Rotation` | int | 0 | -360 .. 360 | [VC: `E_VALUECURVE_Ripple_Rotation`] Rotates the ripple shape by this many degrees. Useful for orienting non-circular shapes like triangles or stars. |
| `E_TEXTCTRL_Ripple_Twist` | float | 0.0 | -45 .. 45 (raw -450 .. 450, divisor 10) | [VC: `E_VALUECURVE_Ripple_Twist`] [float text with 1 decimal(s) (e.g. 1.0)] Applies increasing rotation to each successive ripple ring, creating a spiral twist effect. Positive and negative values twist in opposite directions. |
| `E_SLIDER_Ripple_XC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Ripple_XC`] Horizontal position of the ripple center as a percentage offset from the model center. |
| `E_SLIDER_Ripple_YC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Ripple_YC`] Vertical position of the ripple center as a percentage offset from the model center. |
| `E_TEXTCTRL_Ripple_Velocity` | float | 0.0 | 0 .. 30 (raw 0 .. 300, divisor 10) | [VC: `E_VALUECURVE_Ripple_Velocity`] [float text with 1 decimal(s) (e.g. 1.0)] Speed at which the ripple center moves across the model in the specified direction. Zero keeps the center stationary. |
| `E_SLIDER_Ripple_Direction` | int | 0 | -360 .. 360 | [VC: `E_VALUECURVE_Ripple_Direction`] Angle in degrees that the ripple center travels when velocity is non-zero. 0 is right, 90 is up, etc. |
| `E_CHECKBOX_Ripple3D` | bool | 0 |  | When enabled, applies a brightness gradient to the ripple rings to simulate a three-dimensional depth effect. |
| `E_CHOICE_Ripple_TimingTrack` | enum |  | (dynamic: timingTracks) | When set, each timing mark triggers a new ripple cycle. Duration controls how long each cycle lasts. |
| `E_TEXTCTRL_Ripple_FilterLabel` | string |  |  | Text filter applied to timing track labels. Only timing marks whose labels match this filter text will trigger a ripple. |
| `E_CHECKBOX_Ripple_FilterRegex` | bool | 0 |  | When enabled, the filter text is treated as a regular expression pattern instead of a plain text match. |
| `E_SLIDER_Ripple_Duration` | int | 1000 | 50 .. 5000 | How long each ripple cycle lasts in milliseconds after a timing mark fires. Only active when a Timing Track is selected. |
| `E_FILEPICKERCTRL_Ripple_SVG` | file |  |  | SVG used when Object to Draw = SVG. |

## Custom controls (set these in the xLights UI if possible)

- `Ripple_SVG`: Path to a simple SVG file whose outline is used as the ripple shape when Object is set to SVG.

## Visibility rules (which settings matter when)

- when `Ripple_Object_To_Draw in ['Star', 'Snow Flake', 'Polygon']`: enable RIPPLE_POINTS
- when `Ripple_Object_To_Draw in ['Star', 'Snow Flake', 'Polygon']`: enable Ripple_Rotation
- when `Ripple_Draw_Style != 'Old'`: enable Ripple_Rotation
- when `Ripple_Draw_Style != 'Old'`: enable Ripple_Scale, Ripple_Spacing, Ripple_Twist, Ripple_Direction, Ripple_Velocity, Ripple_Outline
- when `Ripple_TimingTrack not in ['']`: enable Ripple_FilterLabel, Ripple_FilterRegex, Ripple_Duration
- when `Ripple_TimingTrack in ['']`: disable Ripple_FilterLabel, Ripple_FilterRegex, Ripple_Duration
