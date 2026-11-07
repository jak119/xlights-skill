# Kaleidoscope effect

The Kaleidoscope effect distorts the pixels in the layers below it. The Canvas option in Layer Blending must be enabled for it to work.

XML: `<Effect name="Kaleidoscope" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

**Canvas effect**: set `T_CHECKBOX_Canvas=1`; it transforms the layers below it.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Kaleidoscope_Type` | enum | Triangle | Triangle, Square, Square 2, 6-Fold, 8-Fold, 12-Fold, Radial | Selects the symmetry pattern used for the kaleidoscope reflection. Triangle and Square use edge-based mirroring, while 6/8/12-Fold use triangular tiling for higher-order symmetry, and Radial creates rotational segment repetition. |
| `E_SLIDER_Kaleidoscope_X` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Kaleidoscope_X`] Horizontal position of the kaleidoscope center point as a percentage of the buffer width. |
| `E_SLIDER_Kaleidoscope_Y` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Kaleidoscope_Y`] Vertical position of the kaleidoscope center point as a percentage of the buffer height. |
| `E_SLIDER_Kaleidoscope_Size` | int | 5 | 2 .. 100 | [VC: `E_VALUECURVE_Kaleidoscope_Size`] Controls the size of the base tile that gets reflected to fill the model. Smaller values create more repetitions; larger values create fewer, bigger reflections. |
| `E_SLIDER_Kaleidoscope_Rotation` | int | 0 | 0 .. 359 | [VC: `E_VALUECURVE_Kaleidoscope_Rotation`] Rotates the entire kaleidoscope pattern around the center point in degrees. |
