# Garlands effect

XML: `<Effect name="Garlands" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Garlands_Type` | int | 0 | 0 .. 4 | Selects the garland droop pattern. Type 0 is flat, types 1-4 create increasingly deep U-shaped sags between attachment points. |
| `E_SLIDER_Garlands_Spacing` | int | 10 | 1 .. 100 | [VC: `E_VALUECURVE_Garlands_Spacing`] Distance between garland rows as a percentage of the buffer size. Higher values spread the rows further apart. |
| `E_TEXTCTRL_Garlands_Cycles` | float | 1.0 | 0 .. 20 (raw 0 .. 200, divisor 10) | [VC: `E_VALUECURVE_Garlands_Cycles`] [float text with 1 decimal(s) (e.g. 1.0)] Number of times the garland animation cycles over the effect duration. Controls the speed of garland movement. |
| `E_CHOICE_Garlands_Direction` | enum | Up | Up, Down, Left, Right, Up then Down, Down then Up, Left then Right, Right then Left | Direction the garlands stack and move. The 'then' options reverse direction at the midpoint of the effect. |
