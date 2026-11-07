# Snowflakes effect

XML: `<Effect name="Snowflakes" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Snowflakes_Count` | int | 5 | 1 .. 100 | [VC: `E_VALUECURVE_Snowflakes_Count`] Maximum number of snowflakes visible on the buffer at the same time. |
| `E_SLIDER_Snowflakes_Type` | int | 1 | 0 .. 9 | Selects the snowflake shape. 0 uses a random mix of all types each frame. Types 1-9 are specific shapes ranging from single pixels to multi-node crosses, diamonds, and squares. |
| `E_SLIDER_Snowflakes_Speed` | int | 10 | 0 .. 50 | [VC: `E_VALUECURVE_Snowflakes_Speed`] Controls how fast snowflakes move. In Driving mode this affects horizontal and vertical scroll speed; in Falling modes it controls the rate of downward movement. |
| `E_CHOICE_Falling` | enum | Driving | Driving, Falling, Falling & Accumulating | Selects the snowflake movement mode. 'Driving' scrolls flakes diagonally across the buffer. 'Falling' drops flakes from top to bottom. 'Falling & Accumulating' drops flakes that pile up at the bottom. |
| `E_SLIDER_Snowflakes_WarmupFrames` | int | 0 | 0 .. 100 | Number of simulation frames to run before the effect starts rendering. This pre-fills the buffer so falling snowflakes appear mid-flight from the first visible frame. |

## Visibility rules (which settings matter when)

- when `Falling == 'Driving'`: disable Snowflakes_WarmupFrames
