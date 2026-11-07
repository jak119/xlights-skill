# Color Wash effect

XML: `<Effect name="Color Wash" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_ColorWash_Cycles` | float | 1.0 | 0.1 .. 20 (raw 1 .. 200, divisor 10) | [VC: `E_VALUECURVE_ColorWash_Cycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of times the full palette color sequence cycles during the effect. Higher values make the color transitions happen faster. |
| `E_CHECKBOX_ColorWash_VFade` | bool | 0 |  | Fades the wash color from full brightness at the vertical center to black at the top and bottom edges. |
| `E_CHECKBOX_ColorWash_HFade` | bool | 0 |  | Fades the wash color from full brightness at the horizontal center to black at the left and right edges. |
| `E_CHECKBOX_ColorWash_ReverseFades` | bool | 0 |  | Reverses the direction of the vertical and horizontal fades so brightness is at the edges and fades to black at the center. |
| `E_CHECKBOX_ColorWash_Shimmer` | bool | 0 |  | Alternates between the current wash color and black on every other frame, creating a rapid strobe-like flicker. |
| `E_CHECKBOX_ColorWash_CircularPalette` | bool | 0 |  | Makes the palette wrap around by blending the last color back into the first, creating a seamless continuous color loop instead of stopping at the last color. |
