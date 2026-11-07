# Circles effect

XML: `<Effect name="Circles" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Circles_Count` | int | 3 | 1 .. 10 | [VC: `E_VALUECURVE_Circles_Count`] Sets the number of circles drawn on the model. In radial mode, controls the number of color rings. |
| `E_SLIDER_Circles_Size` | int | 5 | 1 .. 20 | [VC: `E_VALUECURVE_Circles_Size`] Controls the radius of each circle. In radial mode, this sets the thickness of the concentric rings. |
| `E_SLIDER_Circles_Speed` | int | 10 | 1 .. 30 | [VC: `E_VALUECURVE_Circles_Speed`] Controls how fast the circles move across the model. In radial mode, controls the speed of the outward ring expansion. |
| `E_CHECKBOX_Circles_Bounce` | bool | 0 |  | When enabled, circles bounce off the edges of the model instead of wrapping around to the opposite side. |
| `E_CHECKBOX_Circles_Radial` | bool | 0 |  | Draws expanding concentric rings radiating outward from the center point, using palette colors in alternating bands. |
| `E_CHECKBOX_Circles_Plasma` | bool | 0 |  | Uses a metaball algorithm where overlapping circle influence fields blend together, creating smooth organic plasma-like shapes. |
| `E_CHECKBOX_Circles_Radial_3D` | bool | 0 |  | Draws expanding concentric rings with a continuously cycling rainbow hue based on distance from center, creating a 3D-like depth effect. |
| `E_CHECKBOX_Circles_Bubbles` | bool | 0 |  | Draws hollow circle outlines instead of filled circles, and launches them upward at slightly random angles to simulate rising bubbles. |
| `E_CHECKBOX_Circles_Linear_Fade` | bool | 0 |  | Makes each circle fade from full brightness at the center to dark at the edge, creating a soft glow effect instead of a solid fill. |
| `E_SLIDER_Circles_XC` | int | 0 | -50 .. 50 | [VC: `E_VALUECURVE_Circles_XC`] Shifts the center point of radial rings horizontally. Only active when Radial or Radial 3D is enabled. |
| `E_SLIDER_Circles_YC` | int | 0 | -50 .. 50 | [VC: `E_VALUECURVE_Circles_YC`] Shifts the center point of radial rings vertically. Only active when Radial or Radial 3D is enabled. |

## Visibility rules (which settings matter when)

- when `Circles_Radial checked OR Circles_Radial_3D checked`: enable Circles_XC, Circles_YC
