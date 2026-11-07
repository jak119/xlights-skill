# Video effect

XML: `<Effect name="Video" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHECKBOX_SynchroniseWithAudio` | bool | 0 |  | When enabled, uses the sequence audio file as the video source and synchronises video playback to the audio timeline position. The picked video file, Start Time, Duration Treatment, and Speed are all overridden by the audio file's properties when this is on. |
| `E_TEXTCTRL_Video_Starttime` | float | 0.00 | 0 .. 0.2 (raw 0 .. 20, divisor 100) | [float text with 2 decimal(s) (e.g. 1.00)] The timestamp in seconds within the video file to begin playback from. Allows skipping an intro or starting mid-video. Maximum updates dynamically once the picked video has been probed. |
| `E_CHOICE_Video_DurationTreatment` | enum | Normal | Normal, Normal No Blue, Loop, Slow/Accelerate, Manual, Manual and Loop | How the video duration maps to the effect duration. Normal plays at native speed, Loop repeats the video, Slow/Accelerate stretches or compresses playback to fit, and Manual allows explicit speed control. |
| `E_TEXTCTRL_Video_Speed` | float | 1.00 | -10 .. 10 (raw -1000 .. 1000, divisor 100) | [VC: `E_VALUECURVE_Video_Speed`] [float text with 2 decimal(s) (e.g. 1.00)] Playback speed multiplier used in Manual duration treatment mode. Negative values play the video in reverse. Use a value curve for acceleration effects. |
| `E_CHECKBOX_Video_AspectRatio` | bool | 0 |  | When enabled, the video is scaled to fit within the buffer while preserving its original aspect ratio, adding black bars if needed. |
| `E_TEXTCTRL_Video_CropLeft` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Video_CropLeft`] Percentage of the video frame to crop from the left edge. Use to remove unwanted portions of the video. |
| `E_TEXTCTRL_Video_CropRight` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Video_CropRight`] Percentage of the video frame visible from the left edge. Values less than 100 crop the right side of the video. |
| `E_TEXTCTRL_Video_CropTop` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Video_CropTop`] Percentage of the video frame visible from the bottom edge. Values less than 100 crop the top of the video. |
| `E_TEXTCTRL_Video_CropBottom` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Video_CropBottom`] Percentage of the video frame to crop from the bottom edge. Use to remove unwanted lower portions of the video. |
| `E_TEXTCTRL_SampleSpacing` | int | 0 | 0 .. 200 | Pixel spacing used when sampling the video frame onto the model. A value of 0 uses default sampling; higher values skip pixels for a coarser look. |
| `E_FILEPICKERCTRL_Video_Filename` | file |  |  | Video file path (relative to the show folder is best). |
| `E_CHECKBOX_Video_TransparentBlack` | bool | 0 |  | Key out dark pixels. |
| `E_TEXTCTRL_Video_TransparentBlack` | int | 0 | 0 .. 300 | Transparent-black brightness threshold. |

## Custom controls (set these in the xLights UI if possible)

- `Video_FilenameBlock`: Video file selection: Select / Clear buttons, animated preview thumbnail, filename label, computed video duration, and a 'Match Effect To Video Duration' button.
- `Video_DurationRow`: Read-only display of the picked video's total duration plus a 'Match Effect To Video Duration' button that resizes the effect on the timeline to match.
- `Video_TransparentBlackRow`: Transparent Black checkbox with an inline brightness threshold slider (0-300). When enabled, video pixels below the threshold are keyed out as transparent.

## Visibility rules (which settings matter when)

- when `SynchroniseWithAudio == True`: disable Video_Starttime, Video_DurationTreatment
