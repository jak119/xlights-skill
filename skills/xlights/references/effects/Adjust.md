# Adjust effect

XML: `<Effect name="Adjust" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

**Canvas effect**: set `T_CHECKBOX_Canvas=1`; it transforms the layers below it.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_CHOICE_Action` | enum | None | None, Adjust By Value, Adjust By Percentage, Set Minimum, Set Maximum, Set Range, Shift With Wrap By Value, Prevent Range, Reverse | The type of channel value adjustment to apply. Options include adding/scaling values, clamping to min/max/range, shifting with wrap, excluding a range, or reversing brightness. |
| `E_SPINCTRL_Value1` | int | 0 | -255 .. 255 | Primary adjustment value. Its meaning depends on the action: offset amount for Adjust By Value, percentage for Adjust By Percentage, minimum for Set Minimum, or lower bound for Set Range. |
| `E_SPINCTRL_Value2` | int | 0 | -255 .. 255 | Secondary adjustment value used by actions that require a range, such as Set Range and Prevent Range, where it defines the upper bound. |
| `E_SPINCTRL_NthChannel` | int | 1 | 1 .. 32 | Apply the adjustment to every Nth channel. A value of 1 adjusts every channel, 2 adjusts every other channel, 3 every third, etc. |
| `E_SPINCTRL_StartingAt` | int | 1 | 1 .. 100 | The first channel number (1-based) to begin applying the adjustment. Channels before this position are left unchanged. |
| `E_SPINCTRL_Count` | int | 0 | 0 .. 10000 | Maximum number of channels to adjust. A value of 0 means adjust all matching channels with no limit. |

## Visibility rules (which settings matter when)

- when `Action in ['None', 'Reverse']`: disable Value1
- when `Action in ['Set Range', 'Prevent Range']`: enable Value2
