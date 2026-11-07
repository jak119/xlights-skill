# Music effect

XML: `<Effect name="Music" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Music_Bars` | int | 20 | 1 .. 100 | Number of vertical bars spread across the model width, each representing a range of notes from the audio spectrum. |
| `E_CHOICE_Music_Type` | enum | Morph | Morph, Bounce, Collide, Separate, On | Animation style for each bar. Morph sweeps color upward, Bounce alternates direction per event, Collide moves colors inward from both edges, Separate moves them outward, and On fills the entire bar height. |
| `E_SLIDER_Music_StartNote` | int | 60 | 0 .. 127 | Lowest MIDI note number to include in the visualization. Notes below this are ignored. |
| `E_SLIDER_Music_EndNote` | int | 80 | 0 .. 127 | Highest MIDI note number to include in the visualization. Notes above this are ignored. |
| `E_SLIDER_Music_Sensitivity` | int | 50 | 0 .. 100 | Threshold for triggering a music event. Lower values detect quieter notes; higher values require louder audio to activate a bar. |
| `E_SLIDER_Music_Offset` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Music_Offset`] Horizontal pixel offset applied to the entire bar display, shifting the visualization left or right on the model. |
| `E_CHECKBOX_Music_Scale` | bool | 0 |  | When enabled, each bar is scaled to fill its proportional share of the model width rather than being a single pixel wide. |
| `E_CHOICE_Music_Scaling` | enum | None | None, Individual Notes, All Notes | Controls how the sensitivity threshold is scaled. None uses a fixed threshold, Individual Notes scales per bar based on each bar's peak, and All Notes scales based on the overall peak volume. |
| `E_CHOICE_Music_Colour` | enum | Distinct | Distinct, Blend, Cycle | How colors from the palette are applied. Distinct assigns color bands by position within each bar, Blend smoothly interpolates between palette colors, and Cycle rotates through colors for each successive music event. |
| `E_CHECKBOX_Music_Fade` | bool | 0 |  | When enabled, the bar colors fade in alpha from bottom to top, creating a transparency gradient within each active bar. |
| `E_CHECKBOX_Music_LogarithmicX` | bool | 0 |  | When enabled, assigns more bars to lower frequencies and fewer to higher frequencies using a logarithmic scale, matching how humans perceive pitch. |
