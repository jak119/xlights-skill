# Faces effect

XML: `<Effect name="Faces" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Faces_FaceDefinition` | enum | Default | (dynamic: faces) | Selects which face definition from the model to use. Face definitions map phonemes to specific nodes or image files on the model. |
| `E_CHOICE_Faces_Eyes` | enum | Auto | Open, Closed, Auto, (off) | Controls the eye state. Open keeps eyes always open, Closed keeps them shut, Auto adds periodic random blinking, and (off) disables eye rendering. |
| `E_CHOICE_Faces_EyeBlinkFrequency` | enum | Normal | Slowest, Slow, Normal, Fast, Fastest | How often automatic eye blinks occur when Eyes is set to Auto. Faster settings produce more frequent blinking. |
| `E_CHOICE_Faces_EyeBlinkDuration` | enum | Normal | Short, Normal, Long, Longer | How long each automatic eye blink lasts when Eyes is set to Auto. Longer durations keep the eyes closed for more frames per blink. |
| `E_CHECKBOX_Faces_Outline` | bool | 0 |  | When enabled, displays the face outline nodes in addition to the mouth and eyes, using the defined outline node group. |
| `E_CHECKBOX_Faces_SuppressShimmer` | bool | 0 |  | When enabled, prevents the shimmer animation on phoneme shapes that are defined with a shimmer suffix in the face definition. |
| `E_CHOICE_Faces_UseState` | enum |  | (dynamic: states) | Selects a state definition to use as the face outline instead of the default outline. Allows combining state effects with face rendering. |
| `E_CHECKBOX_Faces_SuppressWhenNotSinging` | bool | 0 |  | When enabled, the entire face (including outline) is hidden during rest phonemes or when no phoneme is active. Requires a Timing Track. |
| `E_SPINCTRL_Faces_LeadFrames` | int | 0 | 0 .. 1000 | Number of frames to fade in before the first phoneme and fade out after the last phoneme on the timing track. Creates smoother transitions at the start and end of singing. |
| `E_CHECKBOX_Faces_Fade` | bool | 0 |  | When enabled, the face brightness gradually fades during the lead in and lead out frames instead of appearing/disappearing abruptly. |
| `E_CHOICE_Faces_Direction` | enum | none | none, left, right, up, down, up-left, down-left, up-right, down-right, peekaboo, wiggle, zoom in, peekaboo 90, peekaboo 180, peekaboo 270, flag wave, up once, down once, vector, tile-left, tile-right, tile-down, tile-up | Direction the face image moves across the model. Only applies to Matrix type faces. |
| `E_TEXTCTRL_Faces_Speed` | float | 1.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] How fast the face image moves in the chosen direction. Only applies to Matrix type faces. |
| `E_TEXTCTRL_Faces_FrameRateAdj` | float | 1.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] Multiplier for the playback speed of animated GIF face images. Values above 1.0 speed up the animation. Only applies to Matrix type faces. |
| `E_CHECKBOX_Faces_PixelOffsets` | bool | 0 |  | When enabled, the X and Y center offset values are treated as pixel counts rather than percentages of the model dimensions. Only applies to Matrix type faces. |
| `E_CHOICE_Faces_Scaling` | enum | Default (from face) | Default (from face), No Scaling, Scale To Fit, Scale Keep Aspect Ratio, Scale Keep Aspect Ratio Crop | How the face image is resized to fit the model when the face type is Matrix. Default (from face) uses the scaling mode defined on the face definition itself. |
| `E_SLIDER_FacesXC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_FacesXC`] Horizontal offset for the starting position of the face image, as a percentage of the model width. Only applies to Matrix type faces. |
| `E_CHECKBOX_Faces_WrapX` | bool | 0 |  | When enabled, the face image wraps around horizontally so pixels that scroll off one side reappear on the other. Only applies to Matrix type faces. |
| `E_SLIDER_FacesYC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_FacesYC`] Vertical offset for the starting position of the face image, as a percentage of the model height. Only applies to Matrix type faces. |
| `E_SLIDER_FacesEndXC` | int | 0 | -100 .. 100 | Horizontal offset for the ending position of the face image when using the vector movement mode. Only applies to Matrix type faces. |
| `E_SLIDER_FacesEndYC` | int | 0 | -100 .. 100 | Vertical offset for the ending position of the face image when using the vector movement mode. Only applies to Matrix type faces. |
| `E_SLIDER_Faces_StartScale` | int | 100 | 0 .. 1000 | Scale factor for the face image at the start of the effect, as a percentage. 100 is the original size. Only applies to Matrix type faces. |
| `E_SLIDER_Faces_EndScale` | int | 100 | 0 .. 1000 | Scale factor for the face image at the end of the effect. The image smoothly transitions from the start scale to this value over the effect duration. Only applies to Matrix type faces. |
| `E_CHOICE_Faces_TimingTrack` | enum |  | (dynamic: lyricTimingTracks) | Lip-sync source: name of a lyric timing track (its 3rd layer holds phonemes). Leave empty and set E_CHOICE_Faces_Phoneme for a fixed mouth. |
| `E_CHOICE_Faces_Phoneme` | enum |  | AI, E, etc, FV, L, MBP, O, rest, U, WQ | Fixed mouth shape used when no timing track is selected. |
| `E_CHECKBOX_Faces_TransparentBlack` | bool | 0 |  | Matrix faces: key out dark image pixels. |
| `E_TEXTCTRL_Faces_TransparentBlack` | int | 0 | 0 .. 300 | Transparent-black brightness threshold. |

## Custom controls (set these in the xLights UI if possible)

- `Faces_MouthMovements`: Drives the mouth phonemes. Pick a Phoneme for a single fixed mouth shape, or pick a Timing Track with phoneme labels for automatic lip-sync.
- `Faces_TransparentBlackRow`: Transparent Black enable checkbox with an inline brightness threshold slider (0-300). When enabled, face image pixels below the threshold are keyed out as transparent.

## Visibility rules (which settings matter when)

- when `Faces_Outline == True`: enable Faces_UseState
- when `Faces_Eyes == 'Auto'`: enable Faces_EyeBlinkFrequency, Faces_EyeBlinkDuration
- when `Faces_SuppressWhenNotSinging == True`: enable Faces_LeadFrames, Faces_Fade
- when `Faces_Direction == 'vector'`: enable FacesEndXC, FacesEndYC
