# Tendril effect

XML: `<Effect name="Tendril" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Tendril_Movement` | enum | Circle | Random, Square, Circle, Horizontal Zig Zag, Horiz. Zig Zag Return, Vertical Zig Zag, Vert. Zig Zag Return, Music Line, Music Circle, Manual | The path the tendril head follows. Options include geometric patterns like circle and square, zig-zag paths, music-reactive modes, or fully manual control via value curves. |
| `E_TEXTCTRL_Tendril_TuneMovement` | int | 10 | 0 .. 20 | [VC: `E_VALUECURVE_Tendril_TuneMovement`] Controls the magnitude of the tendril head movement. Higher values produce larger, more dramatic movements across the buffer. |
| `E_TEXTCTRL_Tendril_Thickness` | int | 3 | 1 .. 20 | [VC: `E_VALUECURVE_Tendril_Thickness`] The line width of the tendril in pixels. Higher values draw a thicker, more visible tendril strand. |
| `E_TEXTCTRL_Tendril_Friction` | int | 10 | 0 .. 20 | Controls how quickly node velocity decays. Lower values allow nodes to move more freely, while higher values make the tendril more sluggish. |
| `E_TEXTCTRL_Tendril_Dampening` | int | 10 | 0 .. 20 | How much each node is influenced by the velocity of its predecessor. Higher values make the tendril body follow the head more closely. |
| `E_TEXTCTRL_Tendril_Tension` | int | 20 | 0 .. 39 | Controls how quickly the spring force decays along the tendril chain. Higher values keep the tail tighter to the head; lower values let it wave more freely. |
| `E_TEXTCTRL_Tendril_Trails` | int | 1 | 1 .. 20 | Number of parallel tendril strands drawn. Each trail has a slightly different spring constant, creating a ribbon-like appearance. |
| `E_TEXTCTRL_Tendril_Length` | int | 60 | 5 .. 100 | Number of nodes in the tendril chain. More nodes create a longer, more flowing tendril. |
| `E_TEXTCTRL_Tendril_Speed` | int | 10 | 1 .. 10 | How fast the tendril head moves along its chosen path. Higher values make the tendril traverse its pattern more quickly. |
| `E_TEXTCTRL_Tendril_XOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Tendril_XOffset`] Shifts the entire tendril pattern left or right as a percentage of the buffer width. |
| `E_TEXTCTRL_Tendril_YOffset` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Tendril_YOffset`] Shifts the entire tendril pattern up or down as a percentage of the buffer height. |
| `E_TEXTCTRL_Tendril_ManualX` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Tendril_ManualX`] Manually sets the horizontal target position for the tendril head when movement is set to Manual. Use with a value curve to animate the path. |
| `E_TEXTCTRL_Tendril_ManualY` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Tendril_ManualY`] Manually sets the vertical target position for the tendril head when movement is set to Manual. Use with a value curve to animate the path. |

## Visibility rules (which settings matter when)

- when `Tendril_Movement == 'Manual'`: enable Tendril_ManualX, Tendril_ManualY; disable Tendril_TuneMovement
