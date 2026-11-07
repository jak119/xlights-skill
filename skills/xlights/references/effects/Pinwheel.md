# Pinwheel effect

XML: `<Effect name="Pinwheel" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Pinwheel_Arms` | int | 3 | 1 .. 20 | Number of colored arms radiating from the center of the pinwheel. Each arm uses the next color from the palette. |
| `E_SLIDER_Pinwheel_ArmSize` | int | 100 | 0 .. 400 | [VC: `E_VALUECURVE_Pinwheel_ArmSize`] Length of each arm as a percentage of the maximum radius. Values above 100 extend the arms beyond the model edges. |
| `E_SLIDER_Pinwheel_Twist` | int | 0 | -360 .. 360 | [VC: `E_VALUECURVE_Pinwheel_Twist`] Degrees of curvature applied along each arm from center to tip. Positive values twist clockwise, negative values twist counter-clockwise, creating spiral arms. |
| `E_SLIDER_Pinwheel_Thickness` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Pinwheel_Thickness`] Width of each arm as a percentage of the angular space between arms. At 100, adjacent arms touch with no gap between them. |
| `E_SLIDER_Pinwheel_Speed` | int | 10 | 0 .. 50 | [VC: `E_VALUECURVE_Pinwheel_Speed`] Rotation speed of the pinwheel. Higher values make the arms spin faster. |
| `E_SLIDER_Pinwheel_Offset` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Pinwheel_Offset`] Starting angular offset in degrees for the pinwheel arms. Rotates the initial position of the entire pinwheel without affecting the spin animation. |
| `E_CHOICE_Pinwheel_Style` | enum | New Render Method | Old Render Method, New Render Method | Rendering algorithm to use. The new method uses ISPC-accelerated rendering for better performance and fills the entire buffer; the old method draws arms by stepping along radial lines. Existing sequences are migrated to preserve 'Old Render Method' so their look doesn't change. |
| `E_CHECKBOX_Pinwheel_Rotation` | bool | 1 |  | Sets the rotation direction. When checked, the pinwheel spins counter-clockwise; when unchecked, it spins clockwise. |
| `E_CHOICE_Pinwheel_3D` | enum | None | None, 3D, 3D Inverted, Sweep | Applies a brightness or alpha gradient across each arm to simulate depth. 3D fades edges, 3D Inverted fades the center, and Sweep applies a directional gradient from one edge to the other. |
| `E_SLIDER_PinwheelXC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_PinwheelXC`] Horizontal position of the pinwheel center as a percentage offset from the model center. |
| `E_SLIDER_PinwheelYC` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_PinwheelYC`] Vertical position of the pinwheel center as a percentage offset from the model center. |
