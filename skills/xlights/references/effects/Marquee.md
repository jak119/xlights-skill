# Marquee effect

XML: `<Effect name="Marquee" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Mode tabs

- `E_NOTEBOOK_Marquee` = one of 'Settings', 'Position' (default 'Settings').
  - Settings: `E_SLIDER_Marquee_Band_Size`, `E_SLIDER_Marquee_Skip_Size`, `E_SLIDER_Marquee_Thickness`, `E_SLIDER_Marquee_Stagger`, `E_SLIDER_Marquee_Speed`, `E_SLIDER_Marquee_Start`, `E_CHECKBOX_Marquee_Reverse`
  - Position: `E_SLIDER_Marquee_ScaleX`, `E_SLIDER_Marquee_ScaleY`, `E_CHECKBOX_Marquee_PixelOffsets`, `E_SLIDER_MarqueeXC`, `E_CHECKBOX_Marquee_WrapX`, `E_SLIDER_MarqueeYC`, `E_CHECKBOX_Marquee_WrapY`

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Marquee_Band_Size` | int | 3 | 1 .. 100 | [VC: `E_VALUECURVE_Marquee_Band_Size`] Number of consecutive lit pixels in each color band of the marquee pattern. |
| `E_SLIDER_Marquee_Skip_Size` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Marquee_Skip_Size`] Number of unlit (dark) pixels between each color band. Zero means bands are placed back-to-back with no gap. |
| `E_SLIDER_Marquee_Thickness` | int | 1 | 1 .. 100 | [VC: `E_VALUECURVE_Marquee_Thickness`] Number of concentric marquee rings drawn inward from the outer edge. Each ring is offset by one pixel toward the center. |
| `E_SLIDER_Marquee_Stagger` | int | 0 | 0 .. 50 | [VC: `E_VALUECURVE_Marquee_Stagger`] Offsets the starting position of each concentric ring so inner rings appear shifted relative to outer rings, creating a spiral-like look. |
| `E_SLIDER_Marquee_Speed` | int | 3 | 0 .. 50 | [VC: `E_VALUECURVE_Marquee_Speed`] How fast the marquee pattern moves around the perimeter. Zero freezes the animation. |
| `E_SLIDER_Marquee_Start` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Marquee_Start`] Initial offset position for the marquee pattern along the perimeter, allowing the starting point to be adjusted. |
| `E_CHECKBOX_Marquee_Reverse` | bool | 0 |  | When enabled, the marquee pattern moves in the opposite direction around the perimeter. |
| `E_SLIDER_Marquee_ScaleX` | int | 100 | 1 .. 100 | [VC: `E_VALUECURVE_Marquee_ScaleX`] Scales the marquee rectangle width as a percentage. Values below 100 shrink the marquee horizontally. |
| `E_SLIDER_Marquee_ScaleY` | int | 100 | 1 .. 100 | [VC: `E_VALUECURVE_Marquee_ScaleY`] Scales the marquee rectangle height as a percentage. Values below 100 shrink the marquee vertically. |
| `E_CHECKBOX_Marquee_PixelOffsets` | bool | 0 |  | When enabled, the X and Y center offset values are interpreted as absolute pixel counts instead of percentages of the buffer size. |
| `E_SLIDER_MarqueeXC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_MarqueeXC`] Horizontal offset of the marquee center. Shifts the entire marquee rectangle left or right. |
| `E_CHECKBOX_Marquee_WrapX` | bool | 0 |  | When enabled, pixels that move past the left or right edge wrap around to the opposite side instead of being clipped. |
| `E_SLIDER_MarqueeYC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_MarqueeYC`] Vertical offset of the marquee center. Shifts the entire marquee rectangle up or down. |
| `E_CHECKBOX_Marquee_WrapY` | bool | 0 |  | When enabled, pixels that move past the top or bottom edge wrap around to the opposite side instead of being clipped. |
