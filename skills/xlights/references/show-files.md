# The show folder and layout files

An xLights **show folder** holds everything for one display:

| File / folder | What it is | Edit by hand? |
|---|---|---|
| `xlights_rgbeffects.xml` | **Layout**: models, groups, submodels, faces, states, views, preview settings | Carefully, with xLights closed. Prefer the Layout tab. |
| `xlights_networks.xml` | **Controllers**: IPs, protocols, universes/ports | Prefer the Controllers tab. |
| `*.xsq` | Sequences (see `xsq-format.md`) | Yes, with the `xsq.py` helpers |
| `*.fseq` | Rendered output for playback (FPP/xSchedule) | Never; re-render |
| `*.xbkp`, `Backup/` | xLights automatic backups | No (they're your safety net) |
| `xlights_keybindings.xml`, `xlights_effectpresets.json` | UI key bindings, saved effect presets | Rarely |
| `palettes/*.xpalette` | Saved palettes: one line `#rrggbb,#rrggbb,...,` | Yes |
| `valuecurves/*.xvc`, `colorcurves/*.xcc` | Saved curves (`<valuecurve data="..."/>`) | Yes |
| `RenderCache/` | Render cache | Delete freely |
| `Audio/`, `Images/`, `Videos/`, `Shaders/` | Media (convention, any names work) | Yes |

Media paths in sequences can be relative to the show folder (most portable) or to configured media
folders.

## `xlights_rgbeffects.xml`

```xml
<xrgb>
  <models type="rgb_effects">
    <model name="Stairs" DisplayAs="Poly Line" StringType="RGB Nodes" NodesPerString="100" ...
           StartChannel="!Ethernet_:1" Controller="Ethernet_" LayoutGroup="Default"
           WorldPosX="254.29" WorldPosY="122.83" WorldPosZ="0" ...>
      <ControllerConnection Port="1" Protocol="ws2811"/>
      <Aliases><alias name="oldname:string 1"/></Aliases>
      <subModel name="Step 1" layout="horizontal" type="ranges" bufferstyle="Default" line0="1-14"/>
      <faceInfo Name="Singing" Type="NodeRange" Mouth-AI="21-30" Eyes-Open="1-6" .../>
      <stateInfo Name="Countdown" Type="SingleNode" s1="1-5" s1-Name="ten" .../>
    </model>
  </models>
  <modelGroups type="rgb_effects">
    <modelGroup name="All Arches" models="Arch 1,Arch 2,Arch 3" layout="minimalGrid" GridSize="400" .../>
  </modelGroups>
  <view_objects>…</view_objects>   <!-- gridlines, house image, meshes, rulers -->
  <layoutGroups/> <perspectives/> <settings/> <modelSets/> <views/> <colors/> <Viewpoints/>
</xrgb>
```

Get a readable summary with `python3 scripts/xsq.py layout SHOWDIR`.

### Model essentials

- `name`: what sequences reference. Renaming a model breaks sequences unless an
  `<alias name="oldname:Old Name"/>` is added (xLights adds it when you rename in the UI). Names may not
  contain `/` or `,`.
- `DisplayAs`: model type: `Single Line`, `Poly Line`, `Arches`, `Candy Canes`, `Circle`, `Cube`,
  `Custom`, `Icicles`, `Matrix`, `Tree`, `Spinner`, `Sphere`, `Star`, `Window Frame`, `Wreath`,
  `Channel Block`, `Image`, `Label`, `MultiPoint`, and DMX types (`DmxMovingHeadAdv`, `DmxFloodlight`,
  `DmxServo`, `DmxSkull`, `DmxGeneral`...).
- Size: type-specific attributes such as `NumStrings`, `NodesPerString`, `StrandsPerString`, `NumArches`,
  `NodesPerArch`, `CustomWidth/Height` + `CustomModel` data. Older files use `parm1/parm2/parm3`, which
  xLights converts on load.
- `StringType`: `RGB Nodes` (most pixels; colour order such as GRB is usually set on the controller
  port), colour-order variants like `GRB Nodes`, `RGBW Nodes`, `RGBWW Nodes`, `Single Color`,
  `Single Color Red`/`Green`/`Blue`/`White`/`Custom`, `Single Color Intensity`, `Node Single Color`,
  `4 Channel RGBW`, `Strobes`, `Superstring`. Copy the exact value from an existing model when unsure.
- `StartChannel`: `!ControllerName:1` (relative to a controller) is the modern, robust form. Also
  `>OtherModel:1` (chained after the end of another model), `@OtherModel:1` (relative to another
  model's start), `#universe:channel` / `#ip:universe:channel`, or an absolute channel number.
- `<ControllerConnection Port= Protocol= .../>`: which output port and pixel protocol.
- `StartSide` / `Dir`: where node 1 is. Wrong values make chases run backwards.
- Position/scale (`WorldPos*`, `Scale*`, `X2/Y2/Z2`, `PointData`): placement in the preview. This drives
  `Per Preview` rendering across groups.

### Groups

`models` is a comma-separated list of model names. It may include submodels as `Model/Submodel` and other
groups. `layout` is the default render style (`minimalGrid`, `grid`, `horizontal`, `vertical`,
`perModelDefault`...). Groups are sequenced like models (`type="model"` in the `.xsq`).

### Submodels

`<subModel name type="ranges" layout="horizontal|vertical" bufferstyle="Default" line0="1-10" line1="11-20"/>`.
Each `lineN` is one row of the submodel buffer (node ranges `1-10,15,20-25`, 1-based). `type="subbuffer"`
uses `subBuffer="x1xy1xx2xy2"` instead. In sequences, submodel effects go in
`<SubModelEffectLayer name="...">` under the parent model.

### Faces and states

- `faceInfo`: mouth and eye definitions for singing faces. `Type` is `NodeRange` (node lists per phoneme:
  `Mouth-AI`, `Mouth-E`, `Mouth-etc`, `Mouth-FV`, `Mouth-L`, `Mouth-MBP`, `Mouth-O`, `Mouth-U`, `Mouth-WQ`,
  `Mouth-rest`, `Eyes-Open`, `Eyes-Closed`, `FaceOutline`... with optional `-Color` entries), `SingleNode`, or
  `Matrix` (image files per phoneme). Used by the **Faces** effect.
- `stateInfo`: named node sets (`s1`, `s1-Name`, `s1-Color`...) used by the **State** effect (countdown
  digits, on/off segments).

Define faces and states in the xLights model dialogs. Hand-authoring the node lists is error-prone.

## `xlights_networks.xml`

```xml
<Networks computer="...">
  <Controller Id="1" Name="Ethernet_" Type="Ethernet" Vendor="HolidayCoro" Model="AlphaPix Flex"
              IP="192.168.1.17" Protocol="E131" AutoLayout="1" AutoSize="0" ActiveState="Active" ...>
    <network ComPort="192.168.1.17" BaudRate="1" NetworkType="E131" MaxChannels="512"/>  <!-- universe 1 -->
    ...
  </Controller>
</Networks>
```

For E1.31 the `BaudRate` attribute holds the **universe number**. A pixel is 3 channels (RGB), so one
512-channel universe holds 170 RGB pixels (510 channels). Common protocols: `E131` (sACN), `ArtNet`,
`DDP` (no universes; simplest for large pixel counts), `ZCPP`.

## Editing safely

1. **Close xLights** (or at least don't have the Layout tab dirty). xLights keeps the layout in memory and
   overwrites the file on save.
2. Back up both XML files first.
3. Preserve every attribute you don't understand. Change only what you need, with an XML parser, not
   regexes.
4. Reopen xLights and check the Layout tab and model preview.

Model geometry, custom-model grids, DMX channel maps, and controller port assignment are much easier and
safer in the xLights UI. Use file edits for bulk renames (with aliases), creating groups, and auditing.
