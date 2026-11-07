# Twinkle effect

XML: `<Effect name="Twinkle" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Twinkle_Count` | int | 3 | 2 .. 100 | [VC: `E_VALUECURVE_Twinkle_Count`] Percentage of pixels that are actively twinkling at any given time. Higher values create a denser twinkling field. |
| `E_SLIDER_Twinkle_Steps` | int | 30 | 2 .. 400 | [VC: `E_VALUECURVE_Twinkle_Steps`] Number of frames for a complete twinkle cycle (fade up then fade down). Lower values create faster, snappier twinkles; higher values create slow, gentle fades. |
| `E_CHOICE_Twinkle_Style` | enum | New Render Method | Old Render Method, New Render Method | Selects the rendering algorithm. Old Render Method uses the original per-frame logic; New Render Method uses an updated approach with smoother transitions. |
| `E_CHECKBOX_Twinkle_Strobe` | bool | 0 |  | When enabled, twinkling pixels snap on and off instantly instead of fading, creating a strobe-like flash effect. |
| `E_CHECKBOX_Twinkle_ReRandom` | bool | 0 |  | When enabled, each pixel is assigned a new random position after its twinkle cycle completes. When disabled, pixels twinkle in the same locations repeatedly. |
