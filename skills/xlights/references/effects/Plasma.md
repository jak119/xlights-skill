# Plasma effect

XML: `<Effect name="Plasma" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Plasma_Color` | enum | Normal | Normal, Preset Colors 1, Preset Colors 2, Preset Colors 3, Preset Colors 4 | Color scheme for the plasma pattern. Normal uses the effect's palette colors; the preset options use built-in color combinations with different hue ranges. |
| `E_SLIDER_Plasma_Style` | int | 1 | 1 .. 10 | Selects the mathematical formula used to generate the plasma pattern. Higher values produce more complex, twisted interference patterns. |
| `E_SLIDER_Plasma_Line_Density` | int | 1 | 1 .. 10 | Controls how tightly packed the plasma wave lines are. Higher values produce finer, more detailed patterns with more color transitions across the model. |
| `E_SLIDER_Plasma_Speed` | int | 10 | 0 .. 100 | [VC: `E_VALUECURVE_Plasma_Speed`] How fast the plasma pattern animates and flows. Higher values make the waves move more quickly. |
