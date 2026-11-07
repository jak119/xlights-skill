# The `.xsq` sequence file format

Verified against xLights source (`src-core/render/SequenceFile.cpp` `BuildDocument`/`LoadSequence`,
`SequenceElements.cpp` `LoadSequencerFile`) at version 2026.19, and against real sequences.

## Complete minimal example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsequence BaseChannel="0" ChanCtrlBasic="0" ChanCtrlColor="0" FixedPointTiming="1" ModelBlending="true">
  <head>
    <version>2026.19</version>
    <author></author>
    <author-email></author-email>
    <author-website></author-website>
    <song>Wizards in Winter</song>
    <artist>TSO</artist>
    <album></album>
    <MusicURL></MusicURL>
    <comment></comment>
    <sequenceTiming>50 ms</sequenceTiming>
    <sequenceType>Media</sequenceType>
    <mediaFile>Audio/wizards.mp3</mediaFile>
    <sequenceDuration>185.000</sequenceDuration>
    <imageDir></imageDir>
  </head>
  <ColorPalettes>
    <ColorPalette>C_BUTTON_Palette1=#FF0000,C_BUTTON_Palette2=#00FF00,...,C_CHECKBOX_Palette1=1,C_CHECKBOX_Palette2=1,...</ColorPalette>
  </ColorPalettes>
  <EffectDB>
    <Effect>E_CHOICE_Bars_Direction=up,E_SLIDER_Bars_BarCount=1,E_TEXTCTRL_Bars_Cycles=1.0,T_CHECKBOX_Canvas=0,T_CHECKBOX_LayerMorph=0,T_CHOICE_LayerMethod=Normal,T_SLIDER_EffectLayerMix=0</Effect>
  </EffectDB>
  <DataLayers>
    <DataLayer lor_params="0" channel_offset="0" num_channels="0" num_frames="0"
               data="&lt;rendered: erase-mode&gt;" source="&lt;auto-generated&gt;" name="Nutcracker"/>
  </DataLayers>
  <DisplayElements>
    <Element collapsed="0" type="timing" name="Beats" visible="1" views="Master View" active="1"/>
    <Element collapsed="0" type="model" name="Mega Tree" visible="1"/>
  </DisplayElements>
  <ElementEffects>
    <Element type="timing" name="Beats">
      <EffectLayer>
        <Effect label="" startTime="0" endTime="500"/>
        <Effect label="" startTime="500" endTime="1000"/>
      </EffectLayer>
    </Element>
    <Element type="model" name="Mega Tree">
      <EffectLayer>
        <Effect ref="0" name="Bars" startTime="0" endTime="5000" palette="0"/>
      </EffectLayer>
    </Element>
  </ElementEffects>
  <lastView>0</lastView>
  <TimingTags>
    <Tag number="0" position="-1"/>  <!-- ... through number="9" -->
  </TimingTags>
</xsequence>
```

## Section order (important)

xLights loads the file in **one pass** over the root's children. Settings and palettes are looked up by
index when `<ElementEffects>` is read, so:

1. `<head>`
2. `<ColorPalettes>` and `<EffectDB>`: must come **before** `<ElementEffects>`
3. optional: `<SequenceMedia>`, `<FaceDefinitions>`, `<SongStructure>`, `<Jukebox>`, `<EffectSymbols>`
4. `<DataLayers>`
5. `<DisplayElements>`: must come **before** `<ElementEffects>`
6. `<ElementEffects>`
7. `<lastView>`, `<TimingTags>`

Older files may also have `<nextid>`. It's ignored and harmless. Leave optional sections you don't
understand untouched. `<CompressedData size="N">` (base64 zstd) can appear in some files, and xLights inflates
it on load. To edit such a file, open and re-save it in xLights first.

## `<head>`

| Tag | Meaning |
|---|---|
| `version` | xLights version that wrote it (e.g. `2026.19`). Use the user's version if known. |
| `sequenceTiming` | Frame time, **`"<N> ms"`**. 50 ms (20 fps) is the classic default; 25 ms (40 fps) is smoother and common for pixel shows. Every effect time snaps to multiples of this. |
| `sequenceType` | `Media` (has audio) or `Animation` (no audio). |
| `mediaFile` | Audio path. Relative to the show folder or a media folder is most portable; absolute paths also work. |
| `sequenceDuration` | Seconds with 3 decimals, e.g. `185.000`. Should match the audio length. |
| `song`, `artist`, `album`, `author`, `author-email`, `author-website`, `MusicURL`, `comment` | Free text metadata. |
| `imageDir` | Optional folder for images. |
| `altAudioTracks` | Optional `<track shortname="...">path</track>` list. |

Root attributes: keep `FixedPointTiming="1"` (times are integer ms) and `ModelBlending="true"`.

## `<DisplayElements>`: rows shown in the sequencer

One `<Element>` per row, in display order (top to bottom):

- Timing: `type="timing" name="..." visible="1" collapsed="0" views="Master View" active="1"`.
  Only one timing track should be `active="1"` (the one the grid snaps to). The optional `subType` is only used
  for FPP command/effect tracks.
- Model or **model group**: `type="model" name="<exact layout name>" visible="1" collapsed="0"`.
  Groups are also `type="model"`.
- Optional `RenderDisabled="1"` disables rendering of that row.

Booleans may be written `0/1` or `true/false`.

**Every** `<ElementEffects>/<Element>` must have a matching `DisplayElements` entry with the same name
and type, or it's skipped. Names must match `xlights_rgbeffects.xml` exactly (case and spaces). On open,
the GUI offers to rename/map/delete missing models (an `oldname:` alias on a model auto-renames). In
batch or headless render, effects on missing models are **silently dropped**.

## `<ElementEffects>`

### Model element

```xml
<Element type="model" name="Arches">
  <EffectLayer>                 <!-- layer 0 = TOP row in the UI -->
    <Effect ref="3" name="Bars" startTime="0" endTime="5000" palette="1"/>
  </EffectLayer>
  <EffectLayer layerName="base wash">   <!-- layer 1, optional name -->
    <Effect ref="4" name="Color Wash" startTime="0" endTime="20000" palette="2"/>
  </EffectLayer>
  <SubModelEffectLayer name="Arch 1">               <!-- submodel, layer 0 -->
    <Effect ref="5" name="On" startTime="0" endTime="1000" palette="0"/>
  </SubModelEffectLayer>
  <SubModelEffectLayer name="Arch 1" layer="1">     <!-- submodel, layer 1 -->
    ...
  </SubModelEffectLayer>
  <Strand index="0">                                 <!-- strand 0 (e.g. one tree string) -->
    <Effect .../>
    <Node index="12" name="Star tip">                <!-- single node in strand 0 -->
      <Effect .../>
    </Node>
  </Strand>
  <Strand index="0" layer="1">...</Strand>
</Element>
```

- Direct `<EffectLayer>` children come first, then submodel and strand layers.
- `SubModelEffectLayer name` must be a `<subModel name>` defined on that model in the layout.
- A model with no effects still needs one empty `<EffectLayer/>`.
- **Effects in one layer must not overlap in time.** Use another layer to stack effects.
- Keep effects in a layer sorted by `startTime`.

### `<Effect>` attributes (model effects)

| Attr | Required | Meaning |
|---|---|---|
| `name` | yes | Effect type exactly as registered: `On`, `Bars`, `Color Wash`, `SingleStrand`, `VU Meter`, `Moving Head`, `Music`... (see `effects/README.md`). |
| `startTime`, `endTime` | yes | Integer ms. `endTime > startTime` (otherwise the effect is dropped on load). Rounded to the nearest frame multiple on load, so write exact multiples. |
| `ref` | yes* | 0-based index into `<EffectDB>` (the settings string). (*Alternatively the settings can be the element's text content, but always use `ref`.) |
| `palette` | yes | 0-based index into `<ColorPalettes>`. |
| `id` | no | Numeric id (automation API uses it). Omit when writing. |
| `protected` | no | `1` = locked in UI. |
| `selected` | no | UI state; omit. |
| `linkedSymbol` | no | Link to an `<EffectSymbols>` entry; don't create by hand. |

`name="Random"` is never stored (the GUI resolves it to a concrete effect).

### Timing element

```xml
<Element type="timing" name="Beats">
  <EffectLayer>
    <Effect label="1" startTime="0" endTime="480"/>
    <Effect label="2" startTime="480" endTime="960"/>
  </EffectLayer>
</Element>
```

- Marks use `label` (may be empty), `startTime`, `endTime`. No `ref`/`palette`.
- Marks in a layer must not overlap. Normally they're contiguous.
- Fixed-interval track: `<Element type="timing" name="Quarter Notes" fixed="500"><EffectLayer/></Element>`.
  xLights generates marks every `fixed` ms. The interval must be a multiple of the frame time.
- Lyric tracks have **3 layers**: phrases, words, phonemes. See `timing-and-lyrics.md`.

## `<EffectDB>` and `<ColorPalettes>`

Both are de-duplicated lists of settings strings, referenced by index:

- `<EffectDB><Effect>…</Effect></EffectDB>` holds `E_` (effect), `T_` (layer blending/transition) and
  `B_` (buffer) keys.
- `<ColorPalettes><ColorPalette>…</ColorPalette></ColorPalettes>` holds `C_` keys: the 8 colours, their
  enable checkboxes, brightness, sparkles, HSV adjust, chroma key.

Many effects can share one entry. When adding, append a new entry (or reuse an identical one) and point
`ref`/`palette` at its index. **Never renumber or reorder existing entries**, because other effects point at
them. xLights rewrites both lists compactly on its next save.

String encoding: `key=value` pairs joined by `,`, keys sorted alphabetically (xLights's order; not
required). Inside a value, `&` becomes `&amp;` and then `,` becomes `&comma;`. After that comes normal XML escaping, so a
Text effect showing `Merry, Xmas & joy` is stored in the file as
`E_TEXTCTRL_Text=Merry&amp;comma; Xmas &amp;amp; joy`. Let an XML library handle the second step.

Full key reference: `effect-settings.md` and `effects/<Name>.md`.

## `<DataLayers>`

Always include the auto-generated `Nutcracker` layer shown above. Extra data layers hold imported
channel data (LOR/Vixen/fseq); leave them alone.

## `<TimingTags>`

Ten bookmark slots (`number` 0-9, `position` in ms or `-1` unset). Write all ten with `-1` for new files.

## Things xLights stores elsewhere

- Models, groups, submodels, faces, states: `xlights_rgbeffects.xml` (see `show-files.md`).
- Rendered output: `<name>.fseq` (binary, in the show folder or the configured FSEQ folder). It's never
  edited by hand. It's regenerated by rendering.
- Backups: xLights writes `.xbkp` copies and a `Backup/` folder.

## Checklist after editing

- [ ] Section order intact; XML parses.
- [ ] Each ElementEffects element has a DisplayElements twin with the same name and type.
- [ ] Every model/group name exists in the layout. Submodel names exist on their parent.
- [ ] Every `ref`/`palette` index is in range.
- [ ] Times are integers, multiples of the frame time, `start < end`, within the duration.
- [ ] No overlaps within a layer.
- [ ] Settings keys exist for that effect. Timing-track references name real timing tracks.
- [ ] `python3 scripts/xsq.py validate FILE --show SHOWDIR` reports 0 errors.
