# Guitar effect

XML: `<Effect name="Guitar" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Guitar_Type` | enum | Guitar | Guitar, Bass Guitar, Banjo, Violin | Selects the instrument type, which determines the number of strings and tuning used to map MIDI notes to fret positions. |
| `E_CHOICE_Guitar_MIDITrack_APPLYLAST` | enum |  | (dynamic: timingTracks) | The timing track containing MIDI note data that drives the guitar visualization. |
| `E_CHOICE_StringAppearance` | enum | On | On, Wave | How active strings are drawn. On fills a solid band for each string; Wave draws a sine wave oscillation simulating a vibrating string. |
| `E_SLIDER_MaxFrets` | int | 19 | 8 .. 30 | Maximum number of frets on the instrument neck. Higher fret notes are drawn shorter across the buffer width. |
| `E_TEXTCTRL_BaseWaveFactor` | float | 1.0 | 0.1 .. 10 (raw 1 .. 100, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] Base wavelength multiplier for the wave string appearance. Higher values produce longer, smoother waves. |
| `E_TEXTCTRL_StringWaveFactor` | float | 0.0 | 0 .. 10 (raw 0 .. 100, divisor 10) | [float text with 1 decimal(s) (e.g. 1.0)] How much the wavelength varies between strings. Higher values make lower-pitched strings wave more slowly than higher strings. |
| `E_CHECKBOX_Fade` | bool | 0 |  | When enabled, notes fade out over their duration by reducing alpha transparency. |
| `E_CHECKBOX_Collapse` | bool | 0 |  | When enabled, the height of each string's visual shrinks over the note duration, simulating a decaying vibration. |
| `E_CHECKBOX_ShowStrings` | bool | 0 |  | When enabled, draws a thin line for each string beyond the fret position, showing the unfretted portion of the string. |
| `E_CHECKBOX_VaryWaveLengthOnFret` | bool | 1 |  | When enabled, the wave wavelength varies based on fret position so that higher frets produce shorter, tighter waves. |

## Visibility rules (which settings matter when)

- when `StringAppearance == 'Wave'`: enable BaseWaveFactor, StringWaveFactor, VaryWaveLengthOnFret
