# Colour on real LEDs: mixing, gamma, dimming, and palettes that work

What you pick on screen is not what the pixels show. This guide explains why, how to correct for it in
xLights, and how to help a user find palettes that look right **on their own lights**.

## 1. How RGB pixels make colour

Each pixel holds three tiny LEDs (red, green, blue) plus a driver chip. Each channel is a number 0–255
(8-bit), turned into brightness by PWM (flicking the LED on and off fast). Colours mix **additively**,
like light and unlike paint:

| Mix | Result |
|---|---|
| R + G | yellow (more R than G gives orange or amber) |
| R + B | magenta (more B gives purple or violet) |
| G + B | cyan (more B gives sky or ice blue) |
| R + G + B | white (its tint depends on the LED dies) |
| 0, 0, 0 | off. Black is "no light", so it can't be shown on a pixel; it's the absence of light |

Consequences for design:
- **Saturated colours look best.** A single die or two dies at full power give rich colour.
- **Pastels and "tints" wash out.** Pink, lavender, peach, and mint are colour + white, and on pixels they
  often read as "dirty white". Use them deliberately and test them.
- **Dark colours are just dim colours.** Navy is dim blue, maroon is dim red, and brown doesn't exist
  (it comes out dim orange). Dim mixed colours also drift in hue (see §3).
- **Darkness is your contrast colour.** Unlit pixels between lit ones (Bars with black, Skips, Twinkle)
  make colour pop more than a solid wash.

## 2. Why the screen lies

- **Gamma.** Monitors are gamma-encoded (sRGB, about 2.2): the value 128 emits only about 22% of full light,
  which looks like a mid tone. LED PWM is linear, so 128 emits 50% of the light, which the eye sees as
  most of the way to full. Result: mid
  values look much too bright on pixels, mixed colours shift toward the stronger channel, and fades seem
  to "hang" near full and drop off suddenly at the end.
- **Die efficiency.** Green dies look far brighter to the eye than blue at the same value, and red sits in
  between. So `#FFFFFF` often looks cool or blue-green, `#FFA500` "orange" shows as yellow, `#800080`
  "purple" shows as dim magenta or blue, and `#FFC0CB` "pink" shows as near-white.
- **Viewing.** Pixels are point sources seen at night, against darkness, often through diffusers, coroplast,
  or coloured lenses. The house preview in xLights can't show any of that.

## 3. Dimming and low-brightness behaviour

- 8 bits per channel means the bottom of the range is coarse. Steps between 1, 2, 3… out of 255 are big
  visible jumps, and with gamma correction applied the bottom ~10% has even fewer distinct steps. Very
  slow fades to black can look steppy or flicker.
- **Hue drift at low levels.** A warm white like `255,140,60` dimmed to 5% becomes about `13,7,3`, and
  rounding shifts it toward red. Dim mixed colours (amber, warm white, pink) drift more than primaries.
  If you need a dim glow, prefer a primary or near-primary colour, or keep the dim level moderate.
- Some controllers and pixel chips offer higher-bit or dithered output and apply gamma in hardware, which
  gives smoother low-end fades than baking gamma into 8-bit data.
- **Voltage drop.** On long 5 V/12 V runs, blue and green (which need more forward voltage than red) fade
  first, so full white turns yellow, orange, or pink toward the end of a string. That's a power-injection problem,
  not a sequencing one, but it's a common "my white looks wrong" cause. Lowering brightness reduces it.

## 4. Where to correct in xLights (from most to least global)

1. **Controller defaults**: in `xlights_networks.xml`, `DefaultBrightnessUnderFullControl` and
   `DefaultGammaUnderFullControl` (set in the Controllers tab). They're uploaded to controllers that
   support them and apply to every port.
2. **Per model / port**: the model's controller-connection properties (brightness, gamma, colour order,
   null nodes, grouping), uploaded to supporting controllers. Use them to match a brighter or dimmer prop
   type to the rest.
3. **Model dimming curve in xLights**, stored on the model in `xlights_rgbeffects.xml`:
   ```xml
   <dimmingCurve><all gamma="2.2" brightness="0"/></dimmingCurve>
   <!-- or per channel, to colour-balance a mismatched prop: -->
   <dimmingCurve>
     <red gamma="2.2" brightness="0"/><green gamma="2.2" brightness="-15"/><blue gamma="2.2" brightness="0"/>
   </dimmingCurve>
   ```
   Output = (100 + brightness)% × 255 × (value/255)^gamma. `brightness` is a ± percentage offset.
   Per-channel curves fix props whose green is too strong or whose white is too blue. Set them in the
   model's dimming-curve dialog.
4. **In the sequence**: palette colours and `C_SLIDER_Brightness`. This is fine for artistic choices,
   but don't use it to fix hardware differences, or every sequence needs the fix.

Rule of thumb: **fix hardware differences once (controller/model), make artistic choices in sequences.**
Gamma around 2.2 in hardware makes fades look smooth and screen colours match better. Many experienced
sequencers run gamma 2.2–2.8 on pixels. Check what the user already has before changing anything,
because changing gamma changes how every existing sequence looks.

## 5. Every strand is different

Expect variation between, and sometimes within, products:
- **Chip/type**: WS2811 bullets, WS2812B/SK6812 strips, GS8208, UCS1903…, plus RGBW chips with a real white
  die (`RGBW Nodes`, with `RGBWHandling` deciding how white is derived).
- **Manufacturer and batch (binning)**: two orders of "the same" bullets can have different whites and greens.
- **Form factor**: clear vs. diffused bullets, square or flat pixels, seed pixels, strips behind
  diffusion, and pixels pushed into coloured or white coroplast all change perceived colour and brightness.
- **Colour order**: RGB/GRB/BRG… set wrong, red shows as green. Fix it on the controller or model, not in
  the palette.
- **Age and temperature**: older or hot pixels dim and shift.

So **palettes should be tuned per show**, and sometimes a prop gets its own dimming curve. When a user says
"orange looks yellow" or "my whites don't match", it's normal, and fixable.

## 6. Helping a user find palettes that work on their lights

**Colour test sequence.** Build one with `xsq.py color-test` (see SKILL.md), or by hand:
1. A timing track whose labels name each swatch (`#FF4000 orange`, …).
2. For each candidate colour: hold 4–5 s at full on every model (or one model of each type side by side),
   then 4–5 s ramping 100→0 % (`On` with `E_TEXTCTRL_Eff_On_Start=100`, `E_TEXTCTRL_Eff_On_End=0`) to
   check dim-level hue drift and fade smoothness.
3. Include a row of whites: `#FFFFFF`, plus warm candidates like `#FFB060`, `#FF9040`, `#FFC890`.
4. Render, play it on the real display **at night**, and have the user note which swatches look right
   and which look off, for each prop type.
5. Nudge the hex values (orange too yellow → lower green; purple too blue → raise red; white too cool →
   lower blue, then green) and repeat. Save the winners as `palettes/<Name>.xpalette`
   (one line: `#RRGGBB,#RRGGBB,...,` up to 8 colours, trailing comma) so they appear in xLights's palette list.

Ask the user what they're seeing in words ("too yellow", "pinkish white", "looks dim"). Don't assume
their lights match the screen or another person's show.

## 7. Colour theory for show design

- **Colour wheel relationships** (in light, the primaries are R, G, B):
  - Complementary (opposites): red/cyan, green/magenta, blue/yellow-orange. High energy, festive.
    Christmas red/green is near-complementary.
  - Analogous (neighbours): blue/purple/magenta, red/orange/amber. Calm, cohesive, good for ballads.
  - Triadic: R/G/B or orange/purple/green (Halloween). Lively but needs restraint.
  - Monochrome + white: one hue in several brightnesses, plus white sparkles. Elegant and readable.
- **Temperature and mood**: warm (red, orange, amber, warm white) feels cosy, traditional, or spooky-fire.
  Cool (blue, cyan, ice white, purple) feels wintry, magical, or eerie.
- **Limit hues per moment** (2–4). Too many saturated hues at once turns to visual mud from the street.
- **Contrast in brightness as well as hue.** A bright accent over a dim base reads better than two
  equal-brightness colours.
- **Tell a story across the song**: shift palettes at section changes, for example verse cool blues →
  chorus warm golds → finale full rainbow or white.
- **White is powerful**: use it for accents, sparkles, and climaxes. Full white everywhere is flat, and it
  draws the most power.

## 8. Starting-point palettes (tune on real lights!)

These are pixel-friendly starting values that compensate for typical LED behaviour. They aren't
universal. Run a colour test.

| Name | Colours | Notes |
|---|---|---|
| Classic Christmas | `#FF0000` `#00FF00` `#FFFFFF` | Try `#00C000` if green overpowers the red. |
| Warm traditional | `#FF9040` (warm white) `#FF5000` (amber) `#FF0000` | Warm white from RGB: lower blue a lot, green some. |
| Gold & white | `#FF8000` `#FFB040` `#FFE0B0` | Keep blue low for gold. |
| Winter ice | `#0040FF` `#00C0FF` `#A0D0FF` `#FFFFFF` | Cool white = slightly reduced red. |
| Royal | `#6000FF` (purple) `#0000FF` `#FFFFFF` | Purple needs much more blue than red on LEDs. |
| Candy cane | `#FF0000` `#FFFFFF` `#FF0040` | Pink on pixels is mostly red with a little blue. |
| Halloween | `#FF3000` (orange) `#6000FF` (purple) `#20FF00` (slime green) | Orange = full red, small green. |
| Spooky cool | `#00FF40` `#8000FF` `#000000` | Use black in Bars/Spirals for gaps. |
| Patriotic | `#FF0000` `#FFFFFF` `#0000FF` | Use a warm-ish white if the blue looks harsh. |
| Rainbow | `#FF0000` `#FF4000` `#FFC000` `#00FF00` `#00C0FF` `#0000FF` `#8000FF` | Order matters for Bars/Wave. |

Signs you need to adjust: orange or gold looks yellow (lower G); purple looks blue (raise R); pink
looks white (lower G and B); white looks blue or green (lower B, then G); dim colours turn red (raise
the level or pick a purer colour).
