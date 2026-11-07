# Curtain effect

XML: `<Effect name="Curtain" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Curtain_Edge` | enum | left | left, center, right, bottom, middle, top | Sets which edge or pair of edges the curtain opens/closes from. Center and middle split the curtain into two halves that move symmetrically. |
| `E_CHOICE_Curtain_Effect` | enum | open | open, close, open then close, close then open | Controls the curtain motion. Open reveals the model by pulling the curtain away; close covers it. Combined modes perform both actions in sequence within the effect duration. |
| `E_SLIDER_Curtain_Swag` | int | 3 | 0 .. 10 | [VC: `E_VALUECURVE_Curtain_Swag`] Controls the width of the decorative draped curve at the curtain edge. Higher values create a wider parabolic swag that hangs down from the top. |
| `E_TEXTCTRL_Curtain_Speed` | float | 1.0 | 0 .. 10 (raw 0 .. 100, divisor 10) | [VC: `E_VALUECURVE_Curtain_Speed`] [float text with 1 decimal(s) (e.g. 1.0)] Controls how fast the curtain opens or closes. Values above 1 make the curtain complete its motion before the effect ends; values below 1 slow it down. |
| `E_CHECKBOX_Curtain_Repeat` | bool | 0 |  | When enabled, the curtain motion cycles repeatedly for the duration of the effect instead of playing once and stopping. |
