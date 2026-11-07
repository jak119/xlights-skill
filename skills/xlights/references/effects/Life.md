# Life effect

XML: `<Effect name="Life" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_SLIDER_Life_Count` | int | 50 | 0 .. 100 | Percentage of the buffer cells that are initially alive. Higher values create a denser starting population. |
| `E_SLIDER_Life_Seed` | int | 0 | 0 .. 4 | Selects the cellular automaton ruleset: 0=B3/S23 (classic Conway), 1=B35/S236, 2=B357/S1358, 3=B378/S235678, 4=B25678/S5678. Each produces different patterns of growth and decay. |
| `E_SLIDER_Life_Speed` | int | 10 | 1 .. 30 | Controls how fast generations advance. Higher values evolve the cell population more rapidly. |
