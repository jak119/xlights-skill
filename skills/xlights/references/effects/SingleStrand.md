# SingleStrand effect

XML: `<Effect name="SingleStrand" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_SSEFFECT_TYPE` = one of 'Chase', 'Skips', 'FX' (default 'Chase').
  - Chase: `E_CHOICE_SingleStrand_Colors`, `E_SLIDER_Number_Chases`, `E_SLIDER_Color_Mix1`, `E_TEXTCTRL_Chase_Rotations`, `E_CHOICE_SingleStrand_TimingTrack`, `E_TEXTCTRL_Chase_Offset`, `E_CHOICE_Chase_Type1`, `E_CHOICE_Fade_Type`, `E_CHECKBOX_Chase_Group_All`
  - Skips: `E_SLIDER_Skips_BandSize`, `E_SLIDER_Skips_SkipSize`, `E_SLIDER_Skips_StartPos`, `E_SLIDER_Skips_Advance`, `E_CHOICE_Skips_Direction`
  - FX: `E_CHOICE_SingleStrand_FX`, `E_CHOICE_SingleStrand_FX_Palette`, `E_SLIDER_FX_Intensity`, `E_SLIDER_FX_Speed`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_SingleStrand_Colors` | enum | Palette | Rainbow, Palette | Selects the color source for the chase. Palette uses the user-defined palette colors; Rainbow cycles through all hues automatically. |
| `E_SLIDER_Number_Chases` | int | 1 | 1 .. 20 | [VC: `E_VALUECURVE_Number_Chases`] Number of simultaneous chase segments running across the strand. |
| `E_SLIDER_Color_Mix1` | int | 10 | 1 .. 100 | [VC: `E_VALUECURVE_Color_Mix1`] Length of each lit chase segment as a percentage of the total strand length. |
| `E_TEXTCTRL_Chase_Rotations` | float | 1.0 | 0.1 .. 50 (raw 1 .. 500, divisor 10) | [VC: `E_VALUECURVE_Chase_Rotations`] [float text with 1 decimal(s) (e.g. 1.0)] Number of complete chase traversals over the effect duration. Higher values make the chase move faster. |
| `E_CHOICE_SingleStrand_TimingTrack` | enum |  | (dynamic: timingTracks) | When set, the chase performs the Cycles count between each pair of timing marks on this track instead of over the whole effect duration. No chase is drawn before the first mark or after the last mark. |
| `E_TEXTCTRL_Chase_Offset` | float | 0.0 | -500 .. 500 (raw -5000 .. 5000, divisor 10) | [VC: `E_VALUECURVE_Chase_Offset`] [float text with 1 decimal(s) (e.g. 1.0)] Shifts the starting position of the chase pattern along the strand. Useful for staggering chases across multiple models. |
| `E_CHOICE_Chase_Type1` | enum | Left-Right | Left-Right, Right-Left, Bounce from Left, Bounce from Right, Dual Chase, From Middle, To Middle, Bounce to Middle, Bounce from Middle, Static Left-Right, Static Right-Left, Static Dual, Static From Middle, Static To Middle, Static Double-Ended | Direction and movement pattern of the chase. Bounce types reverse at edges, Dual runs two chases simultaneously, Static types display without motion, and Middle types expand or contract from the center. |
| `E_CHOICE_Fade_Type` | enum | None | None, From Head, From Tail, Head and Tail, Middle | Applies a brightness fade to the chase segment. 'From Head' fades from the leading edge, 'From Tail' from the trailing edge, 'Head and Tail' fades both ends, and 'Middle' fades from the center outward. |
| `E_CHECKBOX_Chase_Group_All` | bool | 0 |  | When enabled, treats all strands of the model as one continuous strand for the chase, so the pattern flows seamlessly across strand boundaries. |
| `E_SLIDER_Skips_BandSize` | int | 1 | 1 .. 20 | Number of consecutive lit pixels in each colored band of the skip pattern. |
| `E_SLIDER_Skips_SkipSize` | int | 1 | 0 .. 20 | Number of unlit (dark) pixels between each colored band. Set to 0 for no gaps. |
| `E_SLIDER_Skips_StartPos` | int | 1 | 1 .. 20 | Pixel offset where the first band begins on the strand. |
| `E_SLIDER_Skips_Advance` | int | 0 | 0 .. 100 | Number of times the skip pattern shifts position over the effect duration. Higher values make the pattern appear to march along the strand. |
| `E_CHOICE_Skips_Direction` | enum | Left | Left, Right, From Middle, To Middle | Direction in which the skip pattern is drawn. 'From Middle' and 'To Middle' mirror the pattern from the center of the strand. |
| `E_CHOICE_SingleStrand_FX` | enum | Blink | (dynamic: effect) | Selects which WS2812FX-style animation to run, such as Blink, Breath, Color Wipe, Rainbow, Fire Flicker, and many more. |
| `E_CHOICE_SingleStrand_FX_Palette` | enum | Default | (dynamic: effect) | Selects the color palette mode used by the chosen FX animation, controlling how colors are applied to the effect. |
| `E_SLIDER_FX_Intensity` | int | 128 | 0 .. 255 | [VC: `E_VALUECURVE_FX_Intensity`] Controls the intensity parameter of the selected FX animation. Its exact meaning varies by effect (e.g., brightness, size, or density). |
| `E_SLIDER_FX_Speed` | int | 128 | 0 .. 255 | [VC: `E_VALUECURVE_FX_Speed`] Controls the speed of the selected FX animation. Higher values produce faster transitions and movement. |

## Visibility rules (which settings matter when)

- when `Chase_Type1 starts with 'Static'`: disable Chase_Rotations, SingleStrand_TimingTrack
