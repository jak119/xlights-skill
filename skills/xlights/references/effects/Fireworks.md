# Fireworks effect

XML: `<Effect name="Fireworks" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Fireworks_Explosions` | int | 16 | 1 .. 50 | Total number of firework explosions randomly distributed across the effect duration. Disabled when using music or timing triggers. |
| `E_SLIDER_Fireworks_Count` | int | 50 | 1 .. 100 | [VC: `E_VALUECURVE_Fireworks_Count`] Number of particles created in each explosion. More particles create denser, more dramatic bursts. |
| `E_SLIDER_Fireworks_Velocity` | int | 2 | 1 .. 10 | [VC: `E_VALUECURVE_Fireworks_Velocity`] Maximum speed of particles as they fly outward from the explosion center. Higher values create larger bursts. |
| `E_SLIDER_Fireworks_XVelocity` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Fireworks_XVelocity`] Horizontal drift applied to all particles. Positive values push particles to the right, negative to the left. |
| `E_SLIDER_Fireworks_YVelocity` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Fireworks_YVelocity`] Vertical drift applied to all particles. Positive values push particles upward, negative downward. |
| `E_SLIDER_Fireworks_XLocation` | int | -1 | -1 .. 100 | [VC: `E_VALUECURVE_Fireworks_XLocation`] Fixed horizontal position for explosions as a percentage of buffer width. Set to -1 for random placement. |
| `E_SLIDER_Fireworks_YLocation` | int | -1 | -1 .. 100 | [VC: `E_VALUECURVE_Fireworks_YLocation`] Fixed vertical position for explosions as a percentage of buffer height. Set to -1 for random placement. |
| `E_CHECKBOX_Fireworks_HoldColour` | bool | 1 |  | When enabled, each particle keeps its initial color as it fades. When disabled, particles cycle through the palette as they age. |
| `E_CHECKBOX_Fireworks_Gravity` | bool | 1 |  | When enabled, particles arc downward over time simulating gravity. When disabled, particles fly in straight lines. |
| `E_SLIDER_Fireworks_Fade` | int | 50 | 1 .. 100 | [VC: `E_VALUECURVE_Fireworks_Fade`] How long particles remain visible before fading out. Higher values make particles last longer. |
| `E_CHECKBOX_Fireworks_UseMusic` | bool | 0 |  | When enabled, explosions are triggered by audio volume peaks instead of being evenly distributed. |
| `E_SLIDER_Fireworks_Sensitivity` | int | 50 | 0 .. 100 | Audio volume threshold for triggering explosions when Fire with music is enabled. Lower values trigger more easily. |
| `E_CHECKBOX_FIRETIMING` | bool | 0 |  | When enabled, explosions are triggered at the start and end marks of a selected timing track. |
| `E_CHOICE_FIRETIMINGTRACK` | enum |  | (dynamic: timingTracks) | The timing track whose marks trigger firework explosions when Fire with timing track is enabled. |

## Visibility rules (which settings matter when)

- when `Fireworks_UseMusic == True`: enable Fireworks_Sensitivity
- when `FIRETIMING == True`: enable FIRETIMINGTRACK
- when `FIRETIMING checked OR Fireworks_UseMusic checked`: disable Fireworks_Explosions
