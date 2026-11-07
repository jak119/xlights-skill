# Butterfly effect

XML: `<Effect name="Butterfly" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Butterfly_Colors` | enum | Rainbow | Rainbow, Palette | Selects the color source. Rainbow uses a full HSV rainbow cycle, while Palette uses the user-defined palette colors. |
| `E_SLIDER_Butterfly_Style` | int | 1 | 1 .. 10 | Selects the mathematical pattern formula. Styles 1-5 produce geometric butterfly-like patterns; styles 6-10 generate animated plasma effects. |
| `E_SLIDER_Butterfly_Chunks` | int | 1 | 1 .. 10 | [VC: `E_VALUECURVE_Butterfly_Chunks`] Divides the pattern into repeated segments, increasing the frequency of the mathematical function to create more detailed or tiled patterns. |
| `E_SLIDER_Butterfly_Skip` | int | 2 | 2 .. 10 | [VC: `E_VALUECURVE_Butterfly_Skip`] Controls the spacing interval used when sampling the pattern. Higher values skip more of the pattern, creating a coarser or more spread-out appearance. |
| `E_SLIDER_Butterfly_Speed` | int | 10 | 0 .. 100 | [VC: `E_VALUECURVE_Butterfly_Speed`] Controls how fast the pattern animates. For styles 1-5 this sets the scroll rate; for plasma styles 6-10 higher values produce slower, smoother animation. |
| `E_CHOICE_Butterfly_Direction` | enum | Normal | Normal, Reverse | Sets the animation direction. Reverse inverts the pattern movement so it scrolls in the opposite direction. |
