# Shape effect

XML: `<Effect name="Shape" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Shape_ObjectToDraw` | enum | Circle | Circle, Ellipse, Triangle, Square, Pentagon, Hexagon, Octagon, Star, Heart, Tree, Snowflake, Candy Cane, Random, Crucifix, Present, Emoji, SVG | The geometric shape, holiday object, emoji, or SVG to draw. Random selects a different shape for each new instance. |
| `E_SLIDER_Shape_Thickness` | int | 1 | 1 .. 100 | [VC: `E_VALUECURVE_Shape_Thickness`] Line thickness used to draw the outline of each shape. Higher values produce bolder outlines. |
| `E_TEXTCTRL_Shape_Count` | int | 5 | 1 .. 100 | [VC: `E_VALUECURVE_Shape_Count`] Number of shape instances spawned simultaneously on the model. |
| `E_SLIDER_Shape_StartSize` | int | 1 | 0 .. 100 | [VC: `E_VALUECURVE_Shape_StartSize`] Initial size of each shape when it first appears. The shape then grows or shrinks according to the Growth setting over its lifetime. |
| `E_CHECKBOX_Shape_RandomInitial` | bool | 1 |  | When enabled, each shape starts at a random size and age rather than all beginning at the same start size, creating a more organic initial appearance. |
| `E_SLIDER_Shapes_Velocity` | int | 0 | 0 .. 20 | [VC: `E_VALUECURVE_Shapes_Velocity`] Speed at which each shape moves across the model in the specified direction. Zero keeps shapes stationary. |
| `E_SLIDER_Shapes_Direction` | int | 90 | 0 .. 359 | [VC: `E_VALUECURVE_Shapes_Direction`] Angle in degrees that shapes travel when velocity is non-zero. 0 is right, 90 is up, 180 is left, 270 is down. |
| `E_SLIDER_Shape_Lifetime` | int | 5 | 1 .. 100 | [VC: `E_VALUECURVE_Shape_Lifetime`] How long each shape lives as a percentage of the total effect duration. After this time the shape is removed and a new one may be spawned. |
| `E_SLIDER_Shape_Growth` | int | 10 | -100 .. 100 | [VC: `E_VALUECURVE_Shape_Growth`] Rate at which each shape changes size over its lifetime. Positive values make shapes grow larger, negative values make them shrink. |
| `E_SLIDER_Shape_CentreX` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Shape_CentreX`] Horizontal spawn position for shapes as a percentage of the model width, when random location is disabled. |
| `E_SLIDER_Shape_CentreY` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Shape_CentreY`] Vertical spawn position for shapes as a percentage of the model height, when random location is disabled. |
| `E_SLIDER_Shape_Points` | int | 5 | 2 .. 9 | Number of points on star shapes. Only applies when the Object to Draw is set to Star. |
| `E_SLIDER_Shape_Rotation` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Shape_Rotation`] Rotation angle in degrees applied to each shape. Use a value curve to animate the shapes spinning over time. |
| `E_CHECKBOX_Shape_RandomLocation` | bool | 1 |  | When enabled, each shape spawns at a random position on the model instead of at the X/Y Center position. |
| `E_CHECKBOX_Shapes_RandomMovement` | bool | 0 |  | When enabled, each shape gets a random velocity and direction instead of using the Velocity and Direction settings. |
| `E_CHECKBOX_Shape_FadeAway` | bool | 1 |  | When enabled, shapes gradually become transparent as they age, fading out over their lifetime. |
| `E_CHECKBOX_Shape_HoldColour` | bool | 1 |  | When enabled, each shape keeps the color it was assigned at creation. When disabled, shapes follow the current palette color as it changes. |
| `E_CHECKBOX_Shape_UseMusic` | bool | 0 |  | When enabled, new shapes are spawned in response to audio peaks in the music rather than at regular intervals. |
| `E_SLIDER_Shape_Sensitivity` | int | 50 | 0 .. 100 | Audio volume threshold for triggering new shapes when Fire with music is enabled. Lower values trigger on quieter sounds. |
| `E_CHECKBOX_Shape_FireTiming` | bool | 0 |  | When enabled, new shapes are spawned at each timing mark in the selected timing track instead of at regular intervals. |
| `E_CHOICE_Shape_FireTimingTrack` | enum |  | (dynamic: timingTracks) | Selects which timing track to use for triggering new shapes when Fire with timing track is enabled. |
| `E_TEXTCTRL_Shape_FilterLabel` | string |  |  | Only timing marks whose label matches this text will trigger new shapes. Leave empty to match all marks. |
| `E_CHECKBOX_Shape_FilterReg` | bool | 0 |  | When enabled, the Filter Label is treated as a regular expression for matching timing mark labels instead of a plain text match. |
| `E_FILEPICKERCTRL_SVG` | file |  |  | SVG used when Object to Draw = SVG. |
| `E_FONTPICKER_Shape_Font` | font |  |  | Font for Emoji objects. |
| `E_SPINCTRL_Shape_Char` | int | 127876 |  | Unicode code point for Emoji objects. |
| `E_CHOICE_Shape_SkinTone` | enum |  |  | Emoji skin tone. |

## Custom controls (set these in the xLights UI if possible)

- `Shape_Font`: Font used for rendering emoji characters when Object to Draw is set to Emoji.
- `Shape_Char`: Unicode code point of the emoji or character to display when Object to Draw is set to Emoji.
- `Shape_SkinTone`: Skin tone modifier applied to emoji characters that support it. Only affects emoji rendering.
- `SVG`: Path to an SVG file to use as the shape when Object to Draw is set to SVG.

## Visibility rules (which settings matter when)

- when `Shape_ObjectToDraw in ['Star', 'Ellipse', 'Polygon']`: enable Shape_Points
- when `Shape_ObjectToDraw not in ['Snowflake', 'Emoji']`: enable Shape_Thickness
- when `Shape_ObjectToDraw not in ['Emoji', 'Candy Cane', 'SVG', 'Random', 'Circle']`: enable Shape_Rotation
- when `Shape_ObjectToDraw != 'SVG'`: enable Shape_HoldColour
- when `Shapes_RandomMovement == False`: enable Shapes_Direction, Shapes_Velocity
- when `Shape_RandomLocation == False`: enable Shape_CentreX, Shape_CentreY
- when `Shape_UseMusic == True`: enable Shape_Sensitivity
- when `Shape_FireTiming == True`: enable Shape_FireTimingTrack, Shape_FilterLabel, Shape_FilterReg
