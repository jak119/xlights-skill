# Shimmer effect

XML: `<Effect name="Shimmer" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Shimmer_Duty_Factor` | int | 50 | 1 .. 100 | [VC: `E_VALUECURVE_Shimmer_Duty_Factor`] Percentage of each cycle the color is visible before going black. Lower values produce shorter on-flashes with longer dark gaps. |
| `E_TEXTCTRL_Shimmer_Cycles` | float | 1.0 | 0 .. 600 (raw 0 .. 6000, divisor 10) | [VC: `E_VALUECURVE_Shimmer_Cycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of on/off shimmer cycles over the duration of the effect. Higher values produce faster flickering. |
| `E_CHECKBOX_Shimmer_Use_All_Colors` | bool | 0 |  | When enabled, each pixel is assigned a random color from the palette every frame. When disabled, all pixels use the same color which cycles sequentially through the palette. |
| `E_CHECKBOX_PRE_2017_7` | bool | 0 |  | Uses the legacy shimmer rendering algorithm from before version 2017.7 for backward compatibility with older sequences. |
