# Piano effect

XML: `<Effect name="Piano" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Piano_Type` | enum | True Piano | True Piano, Bars | The visual style for displaying notes. True Piano renders a piano keyboard with keys lighting up; Bars displays horizontal bars for each active note. |
| `E_SPINCTRL_Piano_StartMIDI` | int | 60 | 0 .. 127 | The lowest MIDI note number to display. Notes below this value are ignored. Middle C is 60. |
| `E_SPINCTRL_Piano_EndMIDI` | int | 72 | 0 .. 127 | The highest MIDI note number to display. Together with Start MIDI, defines the visible note range on the keyboard. |
| `E_CHECKBOX_Piano_ShowSharps` | bool | 1 |  | When enabled, black keys (sharps/flats) are rendered on the piano. When disabled, only white keys are shown. |
| `E_CHECKBOX_Piano_FadeNotes` | bool | 0 |  | When enabled, notes gradually fade out over their duration instead of staying at full brightness until they end. |
| `E_CHOICE_Piano_MIDITrack_APPLYLAST` | enum |  | (dynamic: timingTracks) | The timing track containing MIDI note data that drives the piano display. The track must contain note-on/off events. |
| `E_SLIDER_Piano_Scale` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Piano_Scale`] Scales the vertical size of the piano keys or bars as a percentage. Lower values shrink the display; 100 uses the full buffer height. |
| `E_SLIDER_Piano_XOffset` | int | 0 | 0 .. 100 | Shifts the piano display left or right within the buffer. Use to position the keyboard when the note range does not fill the full width. |
