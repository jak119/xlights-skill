# Pictures effect

XML: `<Effect name="Pictures" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Pictures_Direction` | enum | none | none, left, right, up, down, up-left, down-left, up-right, down-right, peekaboo, wiggle, zoom in, peekaboo 90, peekaboo 180, peekaboo 270, flag wave, up once, down once, vector, tile-left, tile-right, tile-down, tile-up | Direction the image moves across the model. Includes scrolling, peekaboo pop-in effects, wiggle, zoom, flag wave, single-pass movements, and tiling modes. |
| `E_TEXTCTRL_Pictures_Speed` | float | 1.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] How fast the image moves in the chosen direction. Higher values make the image scroll or animate more quickly. |
| `E_TEXTCTRL_Pictures_FrameRateAdj` | float | 1.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] Multiplier for the playback speed of animated GIF frames. Values above 1.0 speed up the animation, values below 1.0 slow it down. |
| `E_CHECKBOX_Pictures_PixelOffsets` | bool | 0 |  | When enabled, the X and Y center offset values are treated as pixel counts rather than percentages of the model dimensions. |
| `E_CHOICE_Scaling` | enum | No Scaling | No Scaling, Scale To Fit, Scale Keep Aspect Ratio, Scale Keep Aspect Ratio Crop | How the image is resized to fit the model. No Scaling uses the original pixel size, Scale To Fit stretches to fill, and the aspect ratio options preserve proportions with or without cropping. |
| `E_CHECKBOX_Pictures_Shimmer` | bool | 0 |  | When enabled, the image flickers on and off on alternating frames, creating a shimmering visual effect. |
| `E_CHECKBOX_LoopGIF` | bool | 0 |  | When enabled, an animated GIF restarts from the first frame after reaching the last frame, looping continuously for the duration of the effect. |
| `E_CHECKBOX_SuppressGIFBackground` | bool | 1 |  | When enabled, the background color of an animated GIF is treated as transparent, allowing underlying effects to show through. |
| `E_SLIDER_PicturesXC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_PicturesXC`] Horizontal offset for the starting position of the image, as a percentage of the model width. |
| `E_CHECKBOX_Pictures_WrapX` | bool | 0 |  | When enabled, the image wraps around horizontally so pixels that scroll off one side reappear on the other. |
| `E_SLIDER_PicturesYC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_PicturesYC`] Vertical offset for the starting position of the image, as a percentage of the model height. |
| `E_SLIDER_PicturesEndXC` | int | 0 | -100 .. 100 | Horizontal offset for the ending position of the image when using the vector movement mode. |
| `E_SLIDER_PicturesEndYC` | int | 0 | -100 .. 100 | Vertical offset for the ending position of the image when using the vector movement mode. |
| `E_SLIDER_Pictures_StartScale` | int | 100 | 0 .. 1000 | Scale factor for the image at the start of the effect, as a percentage. 100 is the original size. |
| `E_SLIDER_Pictures_EndScale` | int | 100 | 0 .. 1000 | Scale factor for the image at the end of the effect. The image smoothly transitions from the start scale to this value over the effect duration. |
| `E_TEXTCTRL_Pictures_Filename` | file |  |  | Image/GIF path (relative to the show folder is best). |
| `E_CHECKBOX_Pictures_TransparentBlack` | bool | 0 |  | Key out dark pixels. |
| `E_TEXTCTRL_Pictures_TransparentBlack` | int | 0 | 0 .. 300 | Transparent-black brightness threshold. |

## Custom controls (set these in the xLights UI if possible)

- `Pictures_FilenameBlock`: Image file selection: Select / AI Generate / Clear buttons, animated preview thumbnail, filename label, and a hidden text control that holds the actual path so the saved E_TEXTCTRL_Pictures_Filename round-trips.
- `Pictures_TransparentBlackRow`: Transparent Black checkbox with an inline brightness threshold slider (0-300). When enabled, image pixels at or below the threshold are keyed out as transparent.

## Visibility rules (which settings matter when)

- when `Pictures_Direction == 'vector'`: enable PicturesEndXC, PicturesEndYC
