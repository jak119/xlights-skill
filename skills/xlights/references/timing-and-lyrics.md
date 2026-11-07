# Timing tracks, beats, and lyrics

Timing tracks are the skeleton of a musical sequence. Effects snap to their marks, value curves and
effects can be driven by them, and singing faces read phonemes from them.

## In the `.xsq`

```xml
<DisplayElements>
  <Element collapsed="0" type="timing" name="Beats" visible="1" views="Master View" active="1"/>
</DisplayElements>
<ElementEffects>
  <Element type="timing" name="Beats">
    <EffectLayer>
      <Effect label="1" startTime="0" endTime="476"/>
      <Effect label="2" startTime="476" endTime="952"/>
    </EffectLayer>
  </Element>
</ElementEffects>
```

- Marks: `label` (optional text), `startTime`, `endTime` in integer ms, multiples of the frame time,
  non-overlapping, sorted. Usually contiguous (each mark ends where the next begins).
- Fixed interval: `<Element type="timing" name="Every 500ms" fixed="500"><EffectLayer/></Element>`.
- Timing track names must not collide with model names.
- `xsq.py add-timing SEQ --name Beats --marks 0,476,952,...` builds one from boundary times.

## Lyric tracks (3 layers)

```xml
<Element type="timing" name="Lyrics">
  <EffectLayer>   <!-- layer 0: phrases -->
    <Effect label="Silent night holy night" startTime="12000" endTime="18500"/>
  </EffectLayer>
  <EffectLayer>   <!-- layer 1: words -->
    <Effect label="Silent" startTime="12000" endTime="13100"/> ...
  </EffectLayer>
  <EffectLayer>   <!-- layer 2: phonemes -->
    <Effect label="AI" startTime="12000" endTime="12250"/>
    <Effect label="L" startTime="12250" endTime="12400"/> ...
  </EffectLayer>
</Element>
```

Phoneme labels (Preston Blair set, used by Papagayo and xLights): `AI`, `E`, `etc`, `FV`, `L`, `MBP`,
`O`, `U`, `WQ`, `rest`. The **Faces** effect reads layer 2 of the track named in
`E_CHOICE_Faces_TimingTrack`. Words should sit inside their phrase, and phonemes inside their word.

In the GUI, the usual flow is to type or paste the phrase into a timing track, then let xLights break
phrases into words and words into phonemes using its built-in dictionary (`cmudict`). Lyric files (`.lrc`),
Papagayo (`.pgo`), and subtitle (`.srt`) imports also exist. As an agent you can generate the
3 layers yourself with `Sequence.add_timing(name, layers=[phrases, words, phonemes])`. Then tell the user
to check them in xLights, since phoneme timing usually needs a human pass.

## `.xtiming` files (portable timing export/import)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<timings>
  <timing name="Beats" SourceVersion="2026.19">
    <EffectLayer>
      <Effect label="1" starttime="0" endtime="476" />
    </EffectLayer>
  </timing>
</timings>
```

Note the **lowercase** `starttime`/`endtime` here (the `.xsq` uses camelCase). A single `<timing>` root
also works. Import into a sequence with `xsq.py add-timing SEQ --xtiming file.xtiming`. In xLights, import
it with the timing-track import option.

Other importable formats: Audacity/label `.txt` (`start<TAB>end<TAB>label` in seconds), LOR `.lms`/`.loredit`
timing, Papagayo `.pgo`, `.srt`, `.lrc`.

## Getting good beat timing

Good beat timing takes the most effort and has the biggest payoff in a musical sequence.

1. **Ask the user** whether they already have timing (from xLights's audio analysis, a vendor's
   sequence, or a tap-along track). Human-verified timing beats anything computed.
2. xLights can generate timing from the audio with **VAMP plugins** (for example the Queen Mary bar & beat
   tracker, onset detectors, note transcription). Point the user to this when adding a new timing track.
   An agent can't run it headlessly.
3. If you must compute timing yourself: get the BPM (from the user, or by analysing the audio with a
   library such as `librosa`/`aubio` if available), then `beat_ms = 60000 / BPM`. Lay marks from the
   first downbeat offset and snap each to the frame grid. Provide **bars** (every 4 beats) and **beats** as
   separate tracks. Tempo drift makes long fixed-BPM grids wrong, so say so and suggest spot checks.
4. Build **song structure** too: a track whose marks are labeled `Intro`, `Verse 1`, `Chorus`, `Bridge`,
   `Outro`... Use it to plan the energy curve (see `sequencing-guide.md`).

## Using timing in effects

- Place effect boundaries on marks: chorus effects start exactly on the chorus downbeat, hits on beats.
- Effects with a timing-track option (SingleStrand chase per mark, Shape/Ripple/Fireworks "fire on timing",
  State from labels, Text lyric track) take the **timing track name** as their value.
- Value curves of type `Timing Track Toggle` / `Timing Track Fade Fixed` / `... Proportional` with
  `TT=<track>` pulse any slider on each mark.
- Many short "On" effects, one per beat with a quick fade-out (`T_TEXTCTRL_Fadeout`) or an `On` ramp
  (`E_TEXTCTRL_Eff_On_End=0`), make a classic beat pulse.
