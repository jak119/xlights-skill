# VU Meter effect

XML: `<Effect name="VU Meter" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_VUMeter_Bars` | int | 6 | 1 .. 100 | Number of bars or segments displayed in bar-based VU meter types. Controls the resolution of the frequency or level display. |
| `E_CHOICE_VUMeter_Type` | enum | Waveform | Spectrogram, Spectrogram Peak, Spectrogram Line, Spectrogram Circle Line, Volume Bars, Waveform, Frame Waveform, On, Color On, Dominant Frequency Colour, Dominant Frequency Colour Gradient, Intensity Wave, Pulse, Level Bar, Level Random Bar, Level Color, Level Pulse, Level Jump, Level Jump 100, Level Pulse Color, Level Shape, Timing Event Bar, Timing Event Bar Bounce, Timing Event Random Bar, Timing Event Bars, Timing Event Spike, Timing Event Sweep, Timing Event Sweep 2, Timing Event Timed Sweep, Timing Event Timed Sweep 2, Timing Event Alternate Timed Sweep, Timing Event Alternate Timed Sweep 2, Timing Event Timed Chase From Middle, Timing Event Timed Chase To Middle, Timing Event Color, Timing Event Jump, Timing Event Jump 100, Timing Event Pulse, Timing Event Pulse Color, Note On, Note Level Pulse, Note Level Jump, Note Level Jump 100, Note Level Bar, Note Level Random Bar | The visualization style for the VU meter. Options include spectrogram, volume bars, waveform, timing event responses, level-based displays, note tracking, and more. |
| `E_CHOICE_VUMeter_TimingTrack` | enum |  |  | The timing track used for timing-event-based VU meter types. Events on this track trigger visual responses like spikes, sweeps, and color changes. |
| `E_TEXTCTRL_Filter` | string |  |  | Text filter applied to timing track labels. Only timing events whose labels match this filter text will trigger the VU meter response. |
| `E_CHECKBOX_Regex` | bool | 0 |  | When enabled, the filter text is treated as a regular expression pattern instead of a plain text match. |
| `E_SLIDER_VUMeter_Sensitivity` | int | 70 | 0 .. 100 | Audio level threshold that must be exceeded to trigger the VU meter response. Lower values make it more responsive to quiet sounds. |
| `E_SLIDER_VUMeter_Gain` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_VUMeter_Gain`] Amplifies or attenuates the audio signal level before it drives the visualization. Positive values boost the signal, negative values reduce it. |
| `E_CHOICE_VUMeter_Shape` | enum | Circle | Circle, Filled Circle, Square, Filled Square, Diamond, Filled Diamond, Star, Filled Star, Tree, Filled Tree, Crucifix, Filled Crucifix, Present, Filled Present, Candy Cane, Snowflake, Heart, Filled Heart, SVG | The shape used for level-shape VU meter type. The shape is drawn at a size proportional to the audio level. |
| `E_FILEPICKERCTRL_SVGFile` | file |  |  | Path to an SVG file used as the shape when Shape is set to SVG. The SVG is rendered at a size driven by the audio level. |
| `E_CHECKBOX_VUMeter_SlowDownFalls` | bool | 1 |  | When enabled, bars and levels fall gradually after a peak rather than dropping instantly, creating a smoother visual decay. |
| `E_SLIDER_VUMeter_StartNote` | int | 36 | 0 .. 127 | The lowest MIDI note number included in frequency analysis. Used to focus the spectrogram or note display on a specific pitch range. |
| `E_SLIDER_VUMeter_EndNote` | int | 84 | 0 .. 127 | The highest MIDI note number included in frequency analysis. Together with Start Note, defines the visible pitch range. |
| `E_CHECKBOX_VUMeter_LogarithmicX` | bool | 0 |  | When enabled, the frequency axis uses a logarithmic scale that better matches human pitch perception, giving more space to lower frequencies. |
| `E_SLIDER_VUMeter_XOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_VUMeter_XOffset`] Shifts the VU meter display left or right as a percentage of the buffer width. |
| `E_SLIDER_VUMeter_YOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_VUMeter_YOffset`] Shifts the VU meter display up or down as a percentage of the buffer height. |
| `E_CHOICE_VUMeter_AudioTrack` | enum |  | (dynamic: audioTracks) | Selects which audio track drives this VU Meter. 'Main' uses the sequence's primary audio; additional tracks are listed if alternate audio tracks have been added in Sequence Settings. |

## Visibility rules (which settings matter when)

- when `VUMeter_Type in ['Spectrogram', 'Spectrogram Peak', 'Spectrogram Circle Line', 'Spectrogram Line']`: enable VUMeter_LogarithmicX
- when `VUMeter_Type in ['Volume Bars', 'Waveform', 'Frame Waveform', 'On', 'Color On', 'Intensity Wave', 'Level Bar', 'Level Random Bar', 'Level Color', 'Level Pulse', 'Level Jump', 'Level Jump 100', 'Level Pulse Color', 'Timing Event Jump', 'Note On', 'Note Level Bar', 'Note Level Random Bar', 'Note Level Pulse', 'Note Level Jump', 'Note Level Jump 100', 'Spectrogram Circle Line', 'Level Shape']`: enable VUMeter_Gain
- when `VUMeter_Type in ['Timing Event Spike', 'Timing Event Sweep', 'Timing Event Sweep 2', 'Timing Event Timed Sweep', 'Timing Event Timed Sweep 2', 'Timing Event Alternate Timed Sweep', 'Timing Event Alternate Timed Sweep 2', 'Timing Event Timed Chase To Middle', 'Timing Event Timed Chase From Middle', 'Pulse', 'Timing Event Color', 'Timing Event Pulse', 'Timing Event Bar', 'Timing Event Bar Bounce', 'Timing Event Random Bar', 'Timing Event Bars', 'Timing Event Jump 100', 'Timing Event Pulse Color', 'Timing Event Jump']`: enable VUMeter_TimingTrack, Regex, Filter
- when `VUMeter_Type in ['Level Pulse', 'Level Jump', 'Level Jump 100', 'Level Pulse Color', 'Level Shape', 'Level Bar', 'Level Random Bar', 'Level Color', 'Note Level Bar', 'Note Level Random Bar', 'Spectrogram Peak', 'Spectrogram Line', 'Spectrogram Circle Line', 'Note Level Jump', 'Note Level Jump 100', 'Note Level Pulse', 'Timing Event Color', 'Dominant Frequency Colour', 'Dominant Frequency Colour Gradient']`: enable VUMeter_Sensitivity
- when `VUMeter_Type in ['Level Shape', 'Spectrogram', 'Spectrogram Line', 'Spectrogram Circle Line', 'Spectrogram Peak']`: enable VUMeter_SlowDownFalls
- when `VUMeter_Type in ['Spectrogram', 'Spectrogram Line', 'Spectrogram Circle Line', 'Spectrogram Peak', 'Note On', 'Note Level Bar', 'Note Level Random Bar', 'Note Level Jump', 'Note Level Jump 100', 'Note Level Pulse', 'Dominant Frequency Colour', 'Dominant Frequency Colour Gradient']`: enable VUMeter_StartNote, VUMeter_EndNote
- when `VUMeter_Type in ['Spectrogram', 'Spectrogram Line', 'Spectrogram Circle Line', 'Spectrogram Peak', 'Level Shape']`: enable VUMeter_XOffset
- when `VUMeter_Type in ['Level Shape', 'Spectrogram Circle Line', 'Frame Waveform', 'Waveform']`: enable VUMeter_YOffset
- when `VUMeter_Type == 'Level Shape'`: enable VUMeter_Shape
- when `VUMeter_Type not in ['On', 'Color On', 'Timing Event Color', 'Level Color', 'Note On']`: enable VUMeter_Bars
- when `VUMeter_Type == 'Level Shape' AND VUMeter_Shape == 'SVG'`: enable SVGFile
