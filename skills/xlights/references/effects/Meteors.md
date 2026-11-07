# Meteors effect

XML: `<Effect name="Meteors" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Meteors_Type` | enum | Rainbow | Rainbow, Range, Palette | Color scheme for the meteors. Rainbow uses random hues, Range picks random colors from the palette range, and Palette cycles through the defined palette colors. |
| `E_CHOICE_Meteors_Effect` | enum | Down | Down, Up, Left, Right, Implode, Explode, Icicles, Icicles + bkg | Direction of meteor movement. Down/Up/Left/Right move linearly, Implode moves toward center, Explode moves outward from center, and Icicles create random-length dripping streaks. |
| `E_SLIDER_Meteors_Count` | int | 10 | 1 .. 100 | [VC: `E_VALUECURVE_Meteors_Count`] Number of new meteors spawned per frame. Higher values create a denser shower of meteors. |
| `E_SLIDER_Meteors_Length` | int | 25 | 1 .. 100 | [VC: `E_VALUECURVE_Meteors_Length`] Length of the fading trail behind each meteor. Higher values create longer tails that fade more gradually. |
| `E_SLIDER_Meteors_Swirl_Intensity` | int | 0 | 0 .. 20 | [VC: `E_VALUECURVE_Meteors_Swirl_Intensity`] Adds a random sideways wobble to each meteor as it moves. Higher values create more pronounced swirling motion. |
| `E_SLIDER_Meteors_Speed` | int | 10 | 0 .. 50 | [VC: `E_VALUECURVE_Meteors_Speed`] How fast the meteors travel across the model. Higher values make meteors move more pixels per frame. |
| `E_SLIDER_Meteors_WamupFrames` | int | 0 | 0 .. 100 | Number of simulation frames to run before the first visible frame, so the effect starts with meteors already in flight rather than an empty screen. |
| `E_TEXTCTRL_Meteors_XOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Meteors_XOffset`] Shifts the center point horizontally for Implode and Explode modes. Negative values move the center left, positive values move it right. |
| `E_TEXTCTRL_Meteors_YOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Meteors_YOffset`] Shifts the center point vertically for Implode and Explode modes. Negative values move the center down, positive values move it up. |
| `E_CHECKBOX_Meteors_UseMusic` | bool | 0 |  | When enabled, the meteor count is scaled by the current music volume, producing more meteors during loud passages and fewer during quiet ones. |
| `E_CHECKBOX_FadeWithDistance` | bool | 0 |  | For Implode/Explode modes, meteors fade in brightness based on their distance from center, creating a 3D starfield depth illusion. |

## Visibility rules (which settings matter when)

- when `Meteors_Effect in ['Implode', 'Explode']`: enable Meteors_XOffset, Meteors_YOffset, FadeWithDistance
