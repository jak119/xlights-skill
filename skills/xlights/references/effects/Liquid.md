# Liquid effect

XML: `<Effect name="Liquid" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHECKBOX_TopBarrier` | bool | 0 |  | Places a solid wall along the top edge of the model that prevents particles from escaping upward. |
| `E_CHECKBOX_BottomBarrier` | bool | 1 |  | Places a solid wall along the bottom edge of the model that prevents particles from falling through. |
| `E_CHECKBOX_LeftBarrier` | bool | 0 |  | Places a solid wall along the left edge of the model that prevents particles from escaping to the left. |
| `E_CHECKBOX_RightBarrier` | bool | 0 |  | Places a solid wall along the right edge of the model that prevents particles from escaping to the right. |
| `E_CHECKBOX_HoldColor` | bool | 1 |  | When enabled, particles keep the color they were assigned at creation. When disabled, particle colors are not preserved during rendering. |
| `E_CHECKBOX_MixColors` | bool | 0 |  | When enabled, particles that touch each other blend their colors together over time using the physics engine's color mixing. |
| `E_CHOICE_ParticleType` | enum | Elastic | Powder, Elastic, Spring, Tensile, Viscous, Static Pressure, Water, Reactive, Repulsive | Selects the physics behavior of the particles. Each type has different properties: Water flows freely, Elastic particles bounce, Viscous particles stick together, Powder behaves like sand, etc. |
| `E_TEXTCTRL_LifeTime` | int | 1000 | 0 .. 1000 | [VC: `E_VALUECURVE_LifeTime`] How long each particle lives before disappearing, in hundredths of seconds. A value of 1000 means particles last about 10 seconds. Zero means particles live for the entire effect duration. |
| `E_TEXTCTRL_Size` | int | 500 | 1 .. 10000 | Radius of each particle in thousandths of a pixel. Larger values create bigger, blobby particles; smaller values create fine granular particles. Values above 1000 can slow rendering. |
| `E_TEXTCTRL_WarmUpTime` | int | 0 | 0 .. 25 (raw 0 .. 2500, divisor 100) | How long to run the simulation before the first visible frame, in hundredths of seconds (e.g. 100 = 1 second, 500 = 5 seconds). This lets particles settle into a natural state before the effect begins. Frame-rate independent. |
| `E_TEXTCTRL_Despeckle` | int | 0 | 0 .. 4 | Fills in isolated black pixels surrounded by colored particles. The value is the maximum number of neighboring black pixels allowed before a gap is filled with the average surrounding color. |
| `E_TEXTCTRL_Liquid_Gravity` | float | 10.0 | -100 .. 100 (raw -1000 .. 1000, divisor 10) | [VC: `E_VALUECURVE_Liquid_Gravity`] [float text with 1 decimal(s) (e.g. 1.0)] Strength of the gravitational force applied to particles. Positive values pull in the direction set by Gravity Angle. Negative values push in the opposite direction. |
| `E_TEXTCTRL_Liquid_GravityAngle` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Liquid_GravityAngle`] Direction of gravity in degrees. 0 pulls downward, 90 pulls to the left, 180 pulls upward, and 270 pulls to the right. |
| `E_CHECKBOX_Enabled1` | bool | 1 |  | Enables particle source 1. When disabled, no particles are emitted from this source. |
| `E_TEXTCTRL_X1` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_X1`] Horizontal position of particle source 1 as a percentage of the buffer width. |
| `E_TEXTCTRL_Y1` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_Y1`] Vertical position of particle source 1 as a percentage of the buffer height. |
| `E_TEXTCTRL_Direction1` | int | 270 | 0 .. 360 | [VC: `E_VALUECURVE_Direction1`] Angle in degrees at which particles are emitted from source 1. 0 is right, 90 is up, 180 is left, 270 is down. |
| `E_TEXTCTRL_Velocity1` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Velocity1`] Initial speed of particles emitted from source 1. Higher values launch particles faster in the emission direction. |
| `E_TEXTCTRL_Flow1` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Flow1`] Number of new particles created per frame from source 1. Higher values produce a denser stream of particles. |
| `E_TEXTCTRL_Liquid_SourceSize1` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Liquid_SourceSize1`] Width of the emission area for source 1, spread perpendicular to the emission direction. Zero emits from a point; higher values create a wider spray. |
| `E_CHECKBOX_FlowMusic1` | bool | 0 |  | When enabled, the particle flow rate from source 1 scales with the current music volume level. |
| `E_CHECKBOX_Enabled2` | bool | 0 |  | Enables particle source 2. When disabled, no particles are emitted from this source. |
| `E_TEXTCTRL_X2` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_X2`] Horizontal position of particle source 2 as a percentage of the buffer width. |
| `E_TEXTCTRL_Y2` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Y2`] Vertical position of particle source 2 as a percentage of the buffer height. |
| `E_TEXTCTRL_Direction2` | int | 0 | 0 .. 360 | [VC: `E_VALUECURVE_Direction2`] Angle in degrees at which particles are emitted from source 2. 0 is right, 90 is up, 180 is left, 270 is down. |
| `E_TEXTCTRL_Velocity2` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Velocity2`] Initial speed of particles emitted from source 2. Higher values launch particles faster in the emission direction. |
| `E_TEXTCTRL_Flow2` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Flow2`] Number of new particles created per frame from source 2. Higher values produce a denser stream of particles. |
| `E_TEXTCTRL_Liquid_SourceSize2` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Liquid_SourceSize2`] Width of the emission area for source 2, spread perpendicular to the emission direction. Zero emits from a point; higher values create a wider spray. |
| `E_CHECKBOX_FlowMusic2` | bool | 0 |  | When enabled, the particle flow rate from source 2 scales with the current music volume level. |
| `E_CHECKBOX_Enabled3` | bool | 0 |  | Enables particle source 3. When disabled, no particles are emitted from this source. |
| `E_TEXTCTRL_X3` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_X3`] Horizontal position of particle source 3 as a percentage of the buffer width. |
| `E_TEXTCTRL_Y3` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Y3`] Vertical position of particle source 3 as a percentage of the buffer height. |
| `E_TEXTCTRL_Direction3` | int | 90 | 0 .. 360 | [VC: `E_VALUECURVE_Direction3`] Angle in degrees at which particles are emitted from source 3. 0 is right, 90 is up, 180 is left, 270 is down. |
| `E_TEXTCTRL_Velocity3` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Velocity3`] Initial speed of particles emitted from source 3. Higher values launch particles faster in the emission direction. |
| `E_TEXTCTRL_Flow3` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Flow3`] Number of new particles created per frame from source 3. Higher values produce a denser stream of particles. |
| `E_TEXTCTRL_Liquid_SourceSize3` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Liquid_SourceSize3`] Width of the emission area for source 3, spread perpendicular to the emission direction. Zero emits from a point; higher values create a wider spray. |
| `E_CHECKBOX_FlowMusic3` | bool | 0 |  | When enabled, the particle flow rate from source 3 scales with the current music volume level. |
| `E_CHECKBOX_Enabled4` | bool | 0 |  | Enables particle source 4. When disabled, no particles are emitted from this source. |
| `E_TEXTCTRL_X4` | int | 100 | 0 .. 100 | [VC: `E_VALUECURVE_X4`] Horizontal position of particle source 4 as a percentage of the buffer width. |
| `E_TEXTCTRL_Y4` | int | 50 | 0 .. 100 | [VC: `E_VALUECURVE_Y4`] Vertical position of particle source 4 as a percentage of the buffer height. |
| `E_TEXTCTRL_Direction4` | int | 180 | 0 .. 360 | [VC: `E_VALUECURVE_Direction4`] Angle in degrees at which particles are emitted from source 4. 0 is right, 90 is up, 180 is left, 270 is down. |
| `E_TEXTCTRL_Velocity4` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Velocity4`] Initial speed of particles emitted from source 4. Higher values launch particles faster in the emission direction. |
| `E_TEXTCTRL_Flow4` | int | 100 | 0 .. 1000 | [VC: `E_VALUECURVE_Flow4`] Number of new particles created per frame from source 4. Higher values produce a denser stream of particles. |
| `E_TEXTCTRL_Liquid_SourceSize4` | int | 0 | 0 .. 100 | [VC: `E_VALUECURVE_Liquid_SourceSize4`] Width of the emission area for source 4, spread perpendicular to the emission direction. Zero emits from a point; higher values create a wider spray. |
| `E_CHECKBOX_FlowMusic4` | bool | 0 |  | When enabled, the particle flow rate from source 4 scales with the current music volume level. |

## Visibility rules (which settings matter when)

- when `Enabled1 == True`: enable X1, Y1, Direction1, Velocity1, Flow1, Liquid_SourceSize1, FlowMusic1
- when `Enabled2 == True`: enable X2, Y2, Direction2, Velocity2, Flow2, Liquid_SourceSize2, FlowMusic2
- when `Enabled3 == True`: enable X3, Y3, Direction3, Velocity3, Flow3, Liquid_SourceSize3, FlowMusic3
- when `Enabled4 == True`: enable X4, Y4, Direction4, Velocity4, Flow4, Liquid_SourceSize4, FlowMusic4
