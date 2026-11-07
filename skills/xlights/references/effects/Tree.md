# Tree effect

XML: `<Effect name="Tree" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Tree_Branches` | int | 3 | 1 .. 10 | Number of horizontal branch rows on the tree. The buffer height is divided evenly among branches, with garland lights sweeping across each row. |
| `E_SLIDER_Tree_Speed` | int | 10 | 1 .. 50 | How fast the garland lights sweep across each branch row. Higher values make the animation cycle faster. |
| `E_CHECKBOX_Tree_ShowLights` | bool | 0 |  | When enabled, displays additional twinkling Christmas lights on the tree branches alongside the garland sweep animation. |
