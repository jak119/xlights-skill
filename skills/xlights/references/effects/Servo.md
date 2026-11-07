# Servo effect

XML: `<Effect name="Servo" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Channel` | enum |  | (dynamic: modelNodeNames) | Selects which channel on the DMX model to control. The channel list is populated from the model's node names. |
| `E_CHECKBOX_16bit` | bool | 1 |  | When enabled, outputs a 16-bit value across two channels (coarse and fine) for higher precision servo positioning. When disabled, uses a single 8-bit channel. |
| `E_CHECKBOX_Timing_Track` | bool | 0 |  | When enabled, the servo position is driven by phoneme data from a timing track instead of the start/end value sliders, useful for lip-sync animations. |
| `E_CHOICE_Servo_TimingTrack` | enum |  | (dynamic: lyricTimingTracks) | Selects which timing track to use for phoneme-driven servo positioning when Use Timing Track is enabled. |
| `E_TEXTCTRL_Servo` | float | 0.0 |  | [VC: `E_VALUECURVE_Servo`] Start position 0.0-100.0 %. |
| `E_TEXTCTRL_EndValue` | float | 0.0 |  | End position 0.0-100.0 %. |
| `E_TOGGLEBUTTON_Start` | bool | 0 |  | Link toggle (UI). |
| `E_TOGGLEBUTTON_End` | bool | 0 |  | Link toggle (UI). |

## Custom controls (set these in the xLights UI if possible)

- `Servo_StartEndRow`: Start/End servo position sliders (0-100% as a float with 0.1 precision) with optional value-curve and per-effect link toggles.
- `Servo_ButtonRow`: Sync (mirrors Start and End values), Equal (copies Start to End), and Swap (exchanges Start and End) action buttons.
