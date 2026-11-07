# Duplicate effect

XML: `<Effect name="Duplicate" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Duplicate_Model` | enum |  |  | The source model, submodel, or strand whose effects will be duplicated onto the current model. |
| `E_SPINCTRL_Duplicate_Layer` | int | 1 | 1 .. 1000 | The layer number on the source model to duplicate effects from. Layer 1 is the first (bottom) layer. |
| `E_CHECKBOX_Duplicate_Override_Palette` | bool | 0 |  | When enabled, the color palette from this effect is used instead of the palette from the duplicated source effect. |
| `E_CHECKBOX_Duplicate_Override_Color` | bool | 0 |  | When enabled, the color settings (sparkles, brightness, etc.) from this effect override those from the duplicated source. |
| `E_CHECKBOX_Duplicate_Override_Timing` | bool | 0 |  | When enabled, the layer blending and transition settings from this effect override those from the duplicated source. |
| `E_CHECKBOX_Duplicate_Override_Buffer` | bool | 0 |  | When enabled, the buffer/layer settings (rotation, zoom, etc.) from this effect override those from the duplicated source. |
| `E_CHECKBOX_Duplicate_Include_Submodels` | bool | 0 |  | When enabled, also duplicates effects from matching submodels of the source model onto the corresponding submodels of the current model (matched by name). |
