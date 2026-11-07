# Snowstorm effect

XML: `<Effect name="Snowstorm" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Snowstorm_Count` | int | 50 | 0 .. 100 | Number of snowstorm particles wandering across the buffer. Each particle leaves a fading trail behind it. |
| `E_SLIDER_Snowstorm_Length` | int | 50 | 0 .. 100 | Maximum length of the fading trail behind each particle. Longer trails create streaky, wind-blown looks. |
| `E_SLIDER_Snowstorm_Speed` | int | 10 | 1 .. 50 | Controls how fast each particle moves and how quickly trails grow and decay. Higher values produce more energetic, rapid movement. |
