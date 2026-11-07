# Off effect

This Effect simply turns every pixel off on this model.

If set to be transparent it does not change any pixels.

XML: `<Effect name="Off" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Off_Style` | enum | Black | Black, Transparent, Black -> Transparent, Transparent -> Black | Controls how pixels are turned off. Black sets all pixels to black, Transparent leaves pixels unchanged, and the conversion modes swap black pixels to transparent or vice versa. |
