# Strobe effect

XML: `<Effect name="Strobe" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Number_Strobes` | int | 3 | 1 .. 300 | How many strobe flashes are active at the same time. Higher values create a denser strobe field. |
| `E_SLIDER_Strobe_Duration` | int | 10 | 1 .. 100 | How many frames each strobe flash remains visible before fading out. Higher values make flashes linger longer. |
| `E_SLIDER_Strobe_Type` | int | 1 | 1 .. 4 | Shape of each strobe flash. Type 1 is a single pixel, type 2 adds a random cross arm, type 3 is a full plus shape, and type 4 alternates between plus and X shapes. |
| `E_CHECKBOX_Strobe_Music` | bool | 0 |  | When enabled, the number of active strobes scales with the current music volume level. |
