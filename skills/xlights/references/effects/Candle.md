# Candle effect

XML: `<Effect name="Candle" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_Candle_FlameAgility` | int | 2 | 1 .. 10 | [VC: `E_VALUECURVE_Candle_FlameAgility`] Controls how quickly the flame responds to changes. Higher values make the flame snap to new brightness levels faster, creating a more erratic flicker. |
| `E_TEXTCTRL_Candle_WindBaseline` | int | 30 | 0 .. 255 | [VC: `E_VALUECURVE_Candle_WindBaseline`] Sets the resting wind strength that the simulated wind constantly settles toward. Higher values increase the chance of the wind knocking down the flame. |
| `E_TEXTCTRL_Candle_WindVariability` | int | 5 | 0 .. 10 | [VC: `E_VALUECURVE_Candle_WindVariability`] Controls how often random wind gusts occur. Higher values produce more frequent gusts that disturb the flame. |
| `E_TEXTCTRL_Candle_WindCalmness` | int | 2 | 0 .. 10 | [VC: `E_VALUECURVE_Candle_WindCalmness`] Dampens the wind's effect on the flame. Higher values make the flame more resistant to being blown down, producing a calmer, steadier flicker. |
| `E_CHECKBOX_PerNode` | bool | 0 |  | When enabled, each pixel gets its own independent flame simulation instead of all pixels showing the same flame color. |
| `E_CHECKBOX_UsePalette` | bool | 0 |  | When enabled, the flame color blends between the first two palette colors based on brightness. When disabled, the flame uses a natural orange/yellow candle color. |
