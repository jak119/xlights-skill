# State effect

XML: `<Effect name="State" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_State_StateDefinition` | enum |  | (dynamic: states) | Selects which state definition to use from the model's configured state maps (e.g., SingleNode, NodeRange, or custom state definitions). |
| `E_CHOICE_State_Mode` | enum | Default | Default, Countdown, Time Countdown, Number, Iterate | Controls how timing track labels are interpreted. 'Default' uses labels as state names directly. 'Countdown' treats labels as numbers and counts down. 'Time Countdown' counts down from a time value (MM:SS). 'Number' displays digits for numeric values. 'Iterate' cycles through the listed states over the timing interval. |
| `E_CHOICE_State_Color` | enum | Graduate | Graduate, Cycle, Allocate | Controls how palette colors are assigned to active states. 'Graduate' blends through the palette over time. 'Cycle' assigns a different palette color to each timing interval. 'Allocate' assigns a fixed palette color based on the state's index number. |
| `E_SLIDER_State_Fade_Time` | int | 0 | 0 .. 1000 | Duration in milliseconds for states to fade in and out at the start and end of each timing interval. Set to 0 for instant on/off switching. |
| `E_CHOICE_State_State` | enum |  | (dynamic: states) | State name to show (when driving states directly). Leave empty and set E_CHOICE_State_TimingTrack to drive from timing labels. |
| `E_CHOICE_State_TimingTrack` | enum |  | (dynamic: timingTracks) | Timing track whose mark labels name the state to show at each mark. |

## Custom controls (set these in the xLights UI if possible)

- `State_StateSource`: Choose between selecting a named state directly or driving states from a timing track. Each timing mark's label is matched to a state name.
