# Glediator effect

XML: `<Effect name="Glediator" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_FILEPICKERCTRL_Glediator_Filename` | file |  |  | Path to a Glediator (.gled), Jinx (.out), or CSV file containing pre-rendered pixel data to play back on the model. |
| `E_CHOICE_Glediator_DurationTreatment` | enum | Normal | Normal, Loop, Slow/Accelerate | How to handle timing when the file length differs from the effect duration. Normal stops at the end, Loop restarts from the beginning, Slow/Accelerate stretches or compresses playback to fit. |
