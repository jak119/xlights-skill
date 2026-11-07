#!/usr/bin/env python3
"""xsq.py - read, build, edit and validate xLights sequence (.xsq) files.

Standard library only (Python 3.9+). Use as a CLI or import as a module.

CLI:
  xsq.py info     SEQ.xsq                         summary of a sequence
  xsq.py validate SEQ.xsq [--show DIR]            check structure (+ layout names if --show)
  xsq.py layout   SHOW_DIR                        list models, groups, submodels, faces, states
  xsq.py effect   NAME [--all]                    setting keys/defaults/ranges for an effect
  xsq.py new      OUT.xsq --duration SECS [--frame-ms 50] [--media FILE] [--models A,B,...]
  xsq.py add-effect SEQ.xsq --model M --effect E --start MS --end MS [--layer N]
                    [--submodel S] [--set KEY=VALUE ...] [--colors "#ff0000,#00ff00"]
  xsq.py add-timing SEQ.xsq --name NAME (--marks "0,500,1000,..." | --fixed MS | --xtiming FILE)
  xsq.py color-test OUT.xsq --colors "#FF3000,#6000FF,..." (--show DIR | --models A,B) [--hold 4]
                                                  palette test: each colour full, then fading
  xsq.py vc       EFFECT PROPERTY TYPE [P1 [P2 [P3 [P4]]]]   print a value-curve setting
  xsq.py render   SEQ.xsq --show DIR [--xlights PATH]       headless render to .fseq

Module:
  from xsq import Sequence, load_layout, value_curve
  seq = Sequence.new(duration_s=60, frame_ms=50, media="Audio/song.mp3")
  seq.add_model("Mega Tree")
  seq.add_effect("Mega Tree", "Bars", 0, 5000, settings={"E_CHOICE_Bars_Direction": "down"},
                 colors=["#ff0000", "#00ff00"])
  seq.save("My Song.xsq")

Times are integer milliseconds. Layer 0 is the TOP layer in the xLights UI.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "effects.json"
_EFFECTS = None

# Order xLights writes top-level sections in (SequenceFile::BuildDocument).
# EffectDB/ColorPalettes MUST precede ElementEffects, and DisplayElements must
# precede ElementEffects, because the loader is single-pass.
SECTION_ORDER = ["head", "nextid", "Jukebox", "ColorPalettes", "EffectDB", "SequenceMedia",
                 "FaceDefinitions", "SongStructure", "DataLayers", "EffectSymbols",
                 "DisplayElements", "ElementEffects", "lastView", "TimingTags"]

DEFAULT_PALETTE_COLORS = ["#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
                          "#FFFF00", "#000000", "#00FFFF", "#FF00FF"]

DEFAULT_LAYER_SETTINGS = {
    "T_CHECKBOX_Canvas": "0",
    "T_CHECKBOX_LayerMorph": "0",
    "T_CHOICE_LayerMethod": "Normal",
    "T_SLIDER_EffectLayerMix": "0",
}


# --------------------------------------------------------------------------- data

def effects_db():
    global _EFFECTS
    if _EFFECTS is None:
        with open(DATA) as f:
            _EFFECTS = json.load(f)
    return _EFFECTS


def effect_names():
    return sorted(effects_db()["effects"])


def find_effect(name):
    """Return (canonical_name, entry) for an effect, matching case/space-insensitively."""
    effs = effects_db()["effects"]
    if name in effs:
        return name, effs[name]
    norm = name.replace(" ", "").lower()
    for k, v in effs.items():
        if k.replace(" ", "").lower() == norm:
            return k, v
    raise KeyError(f"Unknown effect '{name}'. Known: {', '.join(sorted(effs))}")


def all_props(effect_name=None):
    """Iterate property dicts for an effect plus the shared Color/Blending/Buffer panels."""
    db = effects_db()
    if effect_name:
        _, e = find_effect(effect_name)
        for p in e["properties"]:
            yield p
    for s in db["shared"].values():
        for p in s["properties"]:
            yield p


def known_keys(effect_name):
    keys = set()
    _, e = find_effect(effect_name)
    for t in e["tabs"]:
        keys.add(t["key"])
    for p in all_props(effect_name):
        if "key" in p:
            keys.add(p["key"])
        if "valueCurve" in p:
            keys.add(p["valueCurve"])
    return keys


def prop_by_key(effect_name, key):
    for p in all_props(effect_name):
        if p.get("key") == key or p.get("valueCurve") == key:
            return p
    return None


def default_settings(effect_name):
    """Settings xLights would write for a freshly dropped effect (metadata defaults)."""
    name, e = find_effect(effect_name)
    out = {}
    for t in e["tabs"]:
        out[t["key"]] = t["default"]
    for p in e["properties"]:
        if p.get("custom") or "key" not in p or p.get("omitIfDefault"):
            continue
        d = p.get("default")
        if d is None or isinstance(d, (list, dict)):
            continue
        if isinstance(d, bool):
            d = 1 if d else 0
        out[p["key"]] = str(d)
    out.update(DEFAULT_LAYER_SETTINGS)
    if e.get("canvasMode"):
        out["T_CHECKBOX_Canvas"] = "1"
    return out


def default_palette():
    pal = {}
    for i, c in enumerate(DEFAULT_PALETTE_COLORS, 1):
        pal[f"C_BUTTON_Palette{i}"] = c
        pal[f"C_CHECKBOX_Palette{i}"] = "1" if i <= 2 else "0"
    pal.update({"C_CHECKBOXBRIGHTNESSLEVEL": "0", "C_CHECKBOX_Chroma": "0",
                "C_CHECKBOX_MusicSparkles": "0", "C_SLIDER_SparkleFrequency": "0"})
    return pal


def make_palette(colors=None, extra=None):
    """Palette dict: `colors` (list of up to 8 '#rrggbb') fill slots 1..n and are enabled;
    remaining slots keep defaults but are disabled. `extra` overlays raw C_ keys."""
    pal = default_palette()
    if colors:
        if len(colors) > 8:
            raise ValueError("A palette has at most 8 colours")
        for i in range(1, 9):
            pal[f"C_CHECKBOX_Palette{i}"] = "0"
        for i, c in enumerate(colors, 1):
            c = c.strip()
            if not c.startswith("#") or len(c) != 7:
                raise ValueError(f"Colour '{c}' must be #rrggbb")
            pal[f"C_BUTTON_Palette{i}"] = c.upper()
            pal[f"C_CHECKBOX_Palette{i}"] = "1"
    if extra:
        pal.update({k: str(v) for k, v in extra.items()})
    return pal


# ---------------------------------------------------------------------- settings

def encode_settings(d):
    """dict -> 'K=V,K=V' string with xLights escaping (sorted keys, like xLights)."""
    parts = []
    for k in sorted(d):
        v = str(d[k]).replace("&", "&amp;").replace(",", "&comma;")
        parts.append(f"{k}={v}")
    return ",".join(parts)


def decode_settings(s):
    out = {}
    if not s:
        return out
    for part in s.split(","):
        if not part:
            continue
        k, _, v = part.partition("=")
        out[k] = v.replace("&comma;", ",").replace("&amp;", "&")
    return out


def _fmt(v):
    v = float(v)
    return f"{v:.2f}"


def value_curve(effect_name, prop, vtype="Ramp", p1=None, p2=None, p3=None, p4=None,
                wrap=False, timing_track=None, extra=None):
    """Build (key, value) for an active value curve on `prop` (property id like
    'Bars_Cycles' or a full key like 'E_TEXTCTRL_Bars_Cycles' / 'C_SLIDER_Brightness').

    P1..P4 are in the property's RAW slider units (same as Min/Max: for divisor
    properties that is value x divisor). E.g. Ramp on Bars_Cycles from 1.0 to 5.0
    cycles: p1=10, p2=50.
    """
    target = None
    for p in all_props(effect_name):
        if "valueCurve" not in p:
            continue
        if prop in (p.get("key"), p.get("valueCurve"), p.get("id")) or \
                (p.get("key", "").split("_", 2)[-1] == prop):
            target = p
            break
    if target is None:
        raise KeyError(f"'{prop}' on {effect_name} does not support value curves")
    vmin = target.get("vcMin", target.get("min", 0))
    vmax = target.get("vcMax", target.get("max", 100))
    key = target["valueCurve"]
    pid = key.split("VALUECURVE_", 1)[1]
    s = f"Active=TRUE|Id=ID_VALUECURVE_{pid}|"
    if vtype != "Flat":
        s += f"Type={vtype}|"
    s += f"Min={_fmt(vmin)}|Max={_fmt(vmax)}|"
    if timing_track:
        s += f"TT={timing_track}|"
    for n, v in (("P1", p1), ("P2", p2), ("P3", p3), ("P4", p4)):
        if v is not None and float(v) != 0:
            s += f"{n}={_fmt(v)}|"
    if wrap:
        s += "WRAP=TRUE|"
    if extra:
        s += extra if extra.endswith("|") else extra + "|"
    s += "RV=TRUE|"
    return key, s


# ------------------------------------------------------------------------ layout

def load_layout(show_dir):
    """Parse xlights_rgbeffects.xml -> {'models': {...}, 'groups': {...}}."""
    path = Path(show_dir) / "xlights_rgbeffects.xml"
    root = ET.parse(path).getroot()
    models, groups = {}, {}
    for m in root.iter("model"):
        name = m.get("name")
        if name is None:
            continue
        models[name] = {
            "type": m.get("DisplayAs"),
            "attrs": dict(m.attrib),
            "submodels": [s.get("name") for s in m.findall("subModel")],
            "faces": [f.get("Name") for f in m.findall("faceInfo")],
            "states": [s.get("Name") for s in m.findall("stateInfo")],
            "aliases": [a.get("name") for a in m.iter("alias")],
            "strands": (m.get("StrandNames") or ""),
        }
    for g in root.iter("modelGroup"):
        groups[g.get("name")] = {
            "models": [x for x in (g.get("models") or "").split(",") if x],
            "layout": g.get("layout"),
            "attrs": dict(g.attrib),
        }
    return {"models": models, "groups": groups, "path": str(path)}


# ---------------------------------------------------------------------- sequence

class Sequence:
    def __init__(self, tree, path=None):
        self.tree = tree
        self.root = tree.getroot()
        self.path = Path(path) if path else None

    # -- construction --------------------------------------------------------
    @classmethod
    def load(cls, path):
        tree = ET.parse(path)
        if tree.getroot().find("CompressedData") is not None:
            raise ValueError("This .xsq has zstd-compressed <CompressedData> sections; "
                             "open and re-save it in xLights first.")
        return cls(tree, path)

    @classmethod
    def new(cls, duration_s, frame_ms=50, media="", version="2026.19", author="", song="",
            artist="", album="", comment="", music_url=""):
        if 1000 % frame_ms and frame_ms not in (15, 30, 60):
            pass  # unusual but allowed; xLights accepts any ms value
        root = ET.Element("xsequence", {"BaseChannel": "0", "ChanCtrlBasic": "0", "ChanCtrlColor": "0",
                                        "FixedPointTiming": "1", "ModelBlending": "true"})
        head = ET.SubElement(root, "head")
        for tag, val in (("version", version), ("author", author), ("author-email", ""),
                         ("author-website", ""), ("song", song), ("artist", artist), ("album", album),
                         ("MusicURL", music_url), ("comment", comment),
                         ("sequenceTiming", f"{int(frame_ms)} ms"),
                         ("sequenceType", "Media" if media else "Animation"),
                         ("mediaFile", media), ("sequenceDuration", f"{float(duration_s):.3f}"),
                         ("imageDir", "")):
            ET.SubElement(head, tag).text = val
        ET.SubElement(root, "ColorPalettes")
        ET.SubElement(root, "EffectDB")
        dl = ET.SubElement(root, "DataLayers")
        ET.SubElement(dl, "DataLayer", {"lor_params": "0", "channel_offset": "0", "num_channels": "0",
                                        "num_frames": "0", "data": "<rendered: erase-mode>",
                                        "source": "<auto-generated>", "name": "Nutcracker"})
        ET.SubElement(root, "DisplayElements")
        ET.SubElement(root, "ElementEffects")
        ET.SubElement(root, "lastView").text = "0"
        tags = ET.SubElement(root, "TimingTags")
        for i in range(10):
            ET.SubElement(tags, "Tag", {"number": str(i), "position": "-1"})
        return cls(ET.ElementTree(root))

    # -- header --------------------------------------------------------------
    def head(self, tag):
        n = self.root.find(f"head/{tag}")
        return n.text if n is not None and n.text else ""

    def set_head(self, tag, value):
        h = self.root.find("head")
        n = h.find(tag)
        if n is None:
            n = ET.SubElement(h, tag)
        n.text = value

    @property
    def frame_ms(self):
        t = self.head("sequenceTiming").replace("ms", "").strip()
        return int(t) if t else 50

    @property
    def duration_ms(self):
        d = self.head("sequenceDuration")
        return int(round(float(d) * 1000)) if d else 0

    # -- sections ------------------------------------------------------------
    def section(self, name):
        n = self.root.find(name)
        if n is not None:
            return n
        n = ET.Element(name)
        my = SECTION_ORDER.index(name)
        idx = len(self.root)
        for i, child in enumerate(list(self.root)):
            if child.tag in SECTION_ORDER and SECTION_ORDER.index(child.tag) > my:
                idx = i
                break
        self.root.insert(idx, n)
        return n

    def effect_strings(self):
        return [e.text or "" for e in self.section("EffectDB").findall("Effect")]

    def palette_strings(self):
        return [p.text or "" for p in self.section("ColorPalettes").findall("ColorPalette")]

    def _intern(self, section, child, s):
        sec = self.section(section)
        for i, n in enumerate(sec.findall(child)):
            if (n.text or "") == s:
                return i
        ET.SubElement(sec, child).text = s
        return len(sec.findall(child)) - 1

    # -- elements ------------------------------------------------------------
    def elements(self):
        return [(e.get("type"), e.get("name")) for e in self.section("DisplayElements").findall("Element")]

    def _effects_element(self, name):
        for e in self.section("ElementEffects").findall("Element"):
            if e.get("name") == name:
                return e
        return None

    def _add_element(self, name, etype):
        if self._effects_element(name) is not None:
            return self._effects_element(name)
        attrs = {"collapsed": "0", "type": etype, "name": name, "visible": "1"}
        if etype == "timing":
            first = not any(t == "timing" for t, _ in self.elements())
            attrs.update({"views": "Master View", "active": "1" if first else "0"})
        ET.SubElement(self.section("DisplayElements"), "Element", attrs)
        el = ET.SubElement(self.section("ElementEffects"), "Element", {"type": etype, "name": name})
        return el

    def add_model(self, name):
        """Add a model or model group row (name must match the layout exactly)."""
        el = self._add_element(name, "model")
        if el.find("EffectLayer") is None:
            ET.SubElement(el, "EffectLayer")
        return el

    def remove_element(self, name):
        for sec in ("DisplayElements", "ElementEffects"):
            s = self.section(sec)
            for e in s.findall("Element"):
                if e.get("name") == name:
                    s.remove(e)

    def _snap(self, ms):
        f = self.frame_ms
        return int(round(int(ms) / f) * f)

    def add_timing(self, name, marks=None, layers=None, fixed=None):
        """Add a timing track.
        marks:  list of boundary times [0, 500, 1000] -> marks 0-500, 500-1000, or
                list of (start, end, label) tuples.
        layers: list of mark-lists for multi-layer (lyric) tracks: [phrases, words, phonemes].
        fixed:  interval in ms for a fixed-interval track (e.g. 500)."""
        el = self._add_element(name, "timing")
        for l in list(el):
            el.remove(l)
        if fixed:
            el.set("fixed", str(self._snap(fixed)))
            ET.SubElement(el, "EffectLayer")
            return el
        for lm in (layers if layers is not None else [marks or []]):
            layer = ET.SubElement(el, "EffectLayer")
            items = []
            if lm and not isinstance(lm[0], (list, tuple)):
                ts = [self._snap(t) for t in lm]
                items = [(a, b, "") for a, b in zip(ts, ts[1:]) if b > a]
            else:
                items = [(self._snap(s), self._snap(e), lab) for s, e, *rest in lm
                         for lab in [rest[0] if rest else ""]]
            for s, e, lab in sorted(items):
                if e <= s:
                    continue
                ET.SubElement(layer, "Effect", {"label": lab, "startTime": str(s), "endTime": str(e)})
        return el

    def timing_tracks(self):
        return [n for t, n in self.elements() if t == "timing"]

    def _layer_node(self, model, layer, submodel=None, create=True):
        el = self._effects_element(model)
        if el is None:
            if not create:
                return None
            el = self.add_model(model)
        if submodel is None:
            layers = el.findall("EffectLayer")
            while len(layers) <= layer:
                if not create:
                    return None
                new = ET.Element("EffectLayer")
                # keep direct EffectLayers before SubModel/Strand layers
                pos = list(el).index(layers[-1]) + 1 if layers else 0
                el.insert(pos, new)
                layers = el.findall("EffectLayer")
            return layers[layer]
        for n in el.findall("SubModelEffectLayer"):
            if n.get("name") == submodel and int(n.get("layer", "0")) == layer:
                return n
        if not create:
            return None
        attrs = {"name": submodel}
        if layer > 0:
            attrs["layer"] = str(layer)
        return ET.SubElement(el, "SubModelEffectLayer", attrs)

    def add_effect(self, model, effect, start, end, layer=0, settings=None, colors=None,
                   palette=None, submodel=None, use_defaults=True, protected=False):
        """Add an effect. `settings` overlays the effect's default settings (E_/T_/B_ keys;
        any C_ keys are moved to the palette). `colors` is a list of '#rrggbb' for the
        palette slots; `palette` overlays raw C_ keys (e.g. {'C_SLIDER_Brightness': 50}).
        Raises ValueError on overlap with an existing effect in the same layer."""
        name, _ = find_effect(effect)
        s, e = self._snap(start), self._snap(end)
        if e <= s:
            raise ValueError(f"end ({e}) must be after start ({s}) after snapping to {self.frame_ms} ms frames")
        st = default_settings(name) if use_defaults else {}
        pal_extra = dict(palette or {})
        for k, v in (settings or {}).items():
            if k.startswith("C_"):
                pal_extra[k] = v
            else:
                st[k] = str(v)
        pal = make_palette(colors, pal_extra)
        ln = self._layer_node(model, layer, submodel)
        for x in ln.findall("Effect"):
            xs, xe = int(x.get("startTime")), int(x.get("endTime"))
            if s < xe and xs < e:
                raise ValueError(f"{model}{'/' + submodel if submodel else ''} layer {layer}: "
                                 f"{s}-{e} overlaps {x.get('name')} {xs}-{xe}")
        ref = self._intern("EffectDB", "Effect", encode_settings(st))
        pref = self._intern("ColorPalettes", "ColorPalette", encode_settings(pal))
        node = ET.Element("Effect", {"ref": str(ref), "name": name, "startTime": str(s),
                                     "endTime": str(e), "palette": str(pref)})
        if protected:
            node.set("protected", "1")
        # keep effects sorted by start time
        kids = ln.findall("Effect")
        pos = len(list(ln))
        for k in kids:
            if int(k.get("startTime")) > s:
                pos = list(ln).index(k)
                break
        ln.insert(pos, node)
        return node

    def iter_effects(self):
        """Yield dicts for every model effect (decoded settings and palette)."""
        db, pals = self.effect_strings(), self.palette_strings()
        for el in self.section("ElementEffects").findall("Element"):
            if el.get("type") != "model":
                continue
            li = 0
            for ln in el:
                if ln.tag == "EffectLayer":
                    where, idx = None, li
                    li += 1
                elif ln.tag == "SubModelEffectLayer":
                    where, idx = ln.get("name"), int(ln.get("layer", "0"))
                elif ln.tag == "Strand":
                    where, idx = f"strand {ln.get('index')}", int(ln.get("layer", "0"))
                else:
                    continue
                for fx in ln.iter("Effect"):
                    ref = fx.get("ref")
                    pal = fx.get("palette")
                    yield {
                        "model": el.get("name"), "sub": where, "layer": idx, "node": fx,
                        "name": fx.get("name"), "start": int(fx.get("startTime", 0)),
                        "end": int(fx.get("endTime", 0)),
                        "settings": decode_settings(db[int(ref)]) if ref and ref.isdigit() and int(ref) < len(db)
                        else decode_settings(fx.text or ""),
                        "palette": decode_settings(pals[int(pal)]) if pal and pal.isdigit() and int(pal) < len(pals) else {},
                    }

    def update_effect(self, node, settings=None, palette=None, remove=(), name=None,
                      start=None, end=None):
        """Change an existing effect (a `node` from iter_effects()['node'] or add_effect()).
        `settings`/`palette` overlay keys (C_ keys go to the palette), `remove` deletes keys.
        A new EffectDB/ColorPalettes entry is interned, so other effects sharing the old one
        are unaffected."""
        db, pals = self.effect_strings(), self.palette_strings()
        ref, pref = node.get("ref"), node.get("palette")
        st = decode_settings(db[int(ref)]) if ref is not None and ref.isdigit() and int(ref) < len(db) else {}
        pal = decode_settings(pals[int(pref)]) if pref is not None and pref.isdigit() and int(pref) < len(pals) else {}
        for k, v in (settings or {}).items():
            (pal if k.startswith("C_") else st)[k] = str(v)
        for k, v in (palette or {}).items():
            pal[k] = str(v)
        for k in remove:
            st.pop(k, None)
            pal.pop(k, None)
        node.set("ref", str(self._intern("EffectDB", "Effect", encode_settings(st))))
        node.set("palette", str(self._intern("ColorPalettes", "ColorPalette", encode_settings(pal))))
        if name:
            node.set("name", find_effect(name)[0])
        if start is not None:
            node.set("startTime", str(self._snap(start)))
        if end is not None:
            node.set("endTime", str(self._snap(end)))
        if int(node.get("endTime")) <= int(node.get("startTime")):
            raise ValueError("end must be after start")
        return node

    def clear_effects(self, model, layer=None, start=None, end=None):
        """Remove effects on a model (optionally one layer / a time window). Returns count."""
        el = self._effects_element(model)
        if el is None:
            return 0
        n = 0
        layers = el.findall("EffectLayer")
        for i, ln in enumerate(layers):
            if layer is not None and i != layer:
                continue
            for fx in ln.findall("Effect"):
                fs, fe = int(fx.get("startTime")), int(fx.get("endTime"))
                if (start is None or fe > start) and (end is None or fs < end):
                    ln.remove(fx)
                    n += 1
        return n

    # -- output --------------------------------------------------------------
    def to_string(self):
        _indent(self.root)
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(self.root, encoding="unicode") + "\n"

    def save(self, path=None, backup=True):
        path = Path(path) if path else self.path
        if path is None:
            raise ValueError("No path given")
        if backup and path.exists():
            stamp = time.strftime("%Y%m%d-%H%M%S")
            shutil.copy2(path, path.with_name(f"{path.stem}.{stamp}.agentbak"))
        tmp = path.with_suffix(".xsq.tmp")
        tmp.write_text(self.to_string(), encoding="utf-8")
        os.replace(tmp, path)
        self.path = path
        return path


def _indent(elem, level=0):
    pad = "\n" + "  " * level
    if len(elem):
        if not (elem.text or "").strip():
            elem.text = pad + "  "
        for child in elem:
            _indent(child, level + 1)
        if not (child.tail or "").strip():
            child.tail = pad
    if level and not (elem.tail or "").strip():
        elem.tail = pad


# -------------------------------------------------------------------- validation

def validate(path, show_dir=None):
    """Return list of (level, message); level is 'ERROR' or 'WARN'."""
    issues = []
    err = lambda m: issues.append(("ERROR", m))
    warn = lambda m: issues.append(("WARN", m))
    try:
        tree = ET.parse(path)
    except ET.ParseError as ex:
        return [("ERROR", f"XML parse error: {ex}")]
    root = tree.getroot()
    if root.tag != "xsequence":
        err(f"root element is <{root.tag}>, expected <xsequence>")
    if root.find("CompressedData") is not None:
        warn("contains <CompressedData> (zstd); contents not checked")
    seq = Sequence(tree, path)
    tags = [c.tag for c in root]
    for a, b in (("EffectDB", "ElementEffects"), ("ColorPalettes", "ElementEffects"),
                 ("DisplayElements", "ElementEffects")):
        if a in tags and b in tags and tags.index(a) > tags.index(b):
            err(f"<{a}> must come before <{b}> (xLights loads in one pass)")
    if root.find("head/sequenceTiming") is None:
        err("missing <head><sequenceTiming> (e.g. '50 ms')")
    fms = seq.frame_ms
    dur = seq.duration_ms
    if dur <= 0:
        err("missing/zero <sequenceDuration>")
    media = seq.head("mediaFile")
    if show_dir and media:
        mp = Path(media)
        if not mp.is_absolute():
            mp = Path(show_dir) / mp
        if not mp.exists():
            warn(f"media file not found: {media} (xLights also searches media folders)")

    db, pals = seq.effect_strings(), seq.palette_strings()
    disp = {}
    for e in root.findall("DisplayElements/Element"):
        n = e.get("name")
        if n in disp:
            err(f"duplicate DisplayElements entry '{n}'")
        disp[n] = e.get("type")
    timing = {n for n, t in disp.items() if t == "timing"}
    seen = set()
    for el in root.findall("ElementEffects/Element"):
        n, t = el.get("name"), el.get("type")
        if n not in disp:
            err(f"ElementEffects '{n}' is not listed in DisplayElements (it will be ignored)")
        elif disp[n] != t:
            err(f"'{n}' is type '{t}' in ElementEffects but '{disp[n]}' in DisplayElements")
        if n in seen:
            err(f"duplicate ElementEffects entry '{n}'")
        seen.add(n)
        if t == "timing":
            for li, ln in enumerate(el.findall("EffectLayer")):
                prev = None
                for fx in ln.findall("Effect"):
                    s, e2 = int(fx.get("startTime", 0)), int(fx.get("endTime", 0))
                    if e2 <= s:
                        err(f"timing '{n}' layer {li}: mark {s}-{e2} has end <= start (dropped)")
                    if prev is not None and s < prev:
                        err(f"timing '{n}' layer {li}: marks overlap or are out of order at {s}")
                    prev = e2
            continue
        # model layers
        for ln in el:
            if ln.tag not in ("EffectLayer", "SubModelEffectLayer", "Strand"):
                continue
            where = n + (f"/{ln.get('name')}" if ln.tag == "SubModelEffectLayer" else
                         f" strand {ln.get('index')}" if ln.tag == "Strand" else "")
            spans = []
            for fx in ln.iter("Effect"):
                s, e2 = int(fx.get("startTime", 0)), int(fx.get("endTime", 0))
                name = fx.get("name", "")
                tag = f"{where} {name}@{s}-{e2}"
                spans.append((s, e2, tag))
                if e2 <= s:
                    err(f"{tag}: end <= start (xLights drops it)")
                if s % fms or e2 % fms:
                    warn(f"{tag}: times not multiples of {fms} ms (will be rounded)")
                if dur and e2 > dur:
                    warn(f"{tag}: ends after sequence duration {dur} ms")
                ref = fx.get("ref")
                if ref is not None:
                    if not ref.isdigit() or int(ref) >= len(db):
                        err(f"{tag}: ref={ref} but EffectDB has {len(db)} entries")
                        continue
                    st = db[int(ref)]
                else:
                    st = fx.text or ""
                pal = fx.get("palette")
                if pal is not None and (not pal.isdigit() or int(pal) >= len(pals)):
                    err(f"{tag}: palette={pal} but ColorPalettes has {len(pals)} entries")
                try:
                    canon, _ = find_effect(name)
                except KeyError:
                    err(f"{tag}: unknown effect name '{name}'")
                    continue
                if canon != name:
                    err(f"{tag}: effect name must be exactly '{canon}'")
                _check_settings(canon, decode_settings(st), tag, timing, err, warn)
                if pal is not None and pal.isdigit() and int(pal) < len(pals):
                    _check_settings(canon, decode_settings(pals[int(pal)]), tag, timing, err, warn, palette=True)
            spans.sort()
            for (a, b, t1), (c, d, t2) in zip(spans, spans[1:]):
                if c < b:
                    err(f"overlapping effects in one layer: {t1} and {t2}")
    for pi, p in enumerate(pals):
        for k in decode_settings(p):
            if not k.startswith("C_"):
                warn(f"ColorPalette {pi}: non-colour key '{k}' (belongs in EffectDB)")

    if show_dir:
        try:
            lay = load_layout(show_dir)
        except (OSError, ET.ParseError) as ex:
            err(f"cannot read layout: {ex}")
        else:
            names = set(lay["models"]) | set(lay["groups"])
            aliases = {a.split(":", 1)[-1].lower(): m for m, d in lay["models"].items() for a in d["aliases"]}
            for n, t in disp.items():
                if t != "model":
                    continue
                if n not in names:
                    if n.lower() in aliases:
                        warn(f"'{n}' is an alias of '{aliases[n.lower()]}': the GUI auto-renames it, "
                             f"but rename it in the file to be safe")
                    else:
                        err(f"model/group '{n}' not in layout - the GUI asks to remap it; "
                            f"batch/headless render silently drops its effects")
            for el in root.findall("ElementEffects/Element"):
                m = lay["models"].get(el.get("name"))
                if not m:
                    continue
                for sm in el.findall("SubModelEffectLayer"):
                    if sm.get("name") not in m["submodels"]:
                        err(f"'{el.get('name')}' has no submodel '{sm.get('name')}'")
            for fx in seq.iter_effects():
                m = lay["models"].get(fx["model"])
                st = fx["settings"]
                if fx["name"] == "Faces" and m is not None:
                    fd = st.get("E_CHOICE_Faces_FaceDefinition", "")
                    if not m["faces"]:
                        warn(f"{fx['model']}: Faces effect but model has no face definitions")
                    elif fd and fd != "Default" and fd not in m["faces"]:
                        err(f"{fx['model']}: face definition '{fd}' not on model (has {m['faces']})")
                if fx["name"] == "State" and m is not None:
                    sd = st.get("E_CHOICE_State_StateDefinition", "")
                    if sd and sd not in m["states"]:
                        err(f"{fx['model']}: state definition '{sd}' not on model (has {m['states']})")
                for k, v in st.items():
                    if "FILEPICKER" in k or k.endswith("_Filename"):
                        if v and not Path(v).is_absolute() and not (Path(show_dir) / v).exists():
                            warn(f"{fx['model']} {fx['name']}@{fx['start']}: file not found: {v}")
    return issues


def _check_settings(effect, st, tag, timing, err, warn, palette=False):
    keys = known_keys(effect)
    for k, v in st.items():
        if not palette and k.startswith("C_"):
            warn(f"{tag}: colour key {k} is in EffectDB; put it in the ColorPalette")
        if k not in keys and not k.startswith(("E_VALUECURVE_", "B_VALUECURVE_", "T_VALUECURVE_", "C_VALUECURVE_")):
            if not (effect == "Shader" and k.startswith("E_")):
                warn(f"{tag}: unrecognised key {k} (typo or legacy?)")
            continue
        if "VALUECURVE_" in k:
            if "Active=TRUE" in v and ("Min=" not in v or "Max=" not in v):
                err(f"{tag}: value curve {k} missing Min/Max")
            continue
        p = prop_by_key(effect, k)
        if not p:
            continue
        if p.get("dynamicOptions") in ("timingTracks", "lyricTimingTracks") and v and v not in timing:
            err(f"{tag}: {k}='{v}' but no timing track with that name")
        opts = p.get("options")
        if isinstance(opts, list) and opts and v not in opts and not p.get("dynamicOptions"):
            warn(f"{tag}: {k}='{v}' not one of {opts}")
        if p.get("type") in ("int",) and "min" in p and "max" in p and "VALUECURVE" not in k:
            try:
                iv = float(v)
                if iv < p["min"] or iv > p["max"]:
                    warn(f"{tag}: {k}={v} outside {p['min']}..{p['max']}")
            except ValueError:
                err(f"{tag}: {k}='{v}' is not a number")
    if effect in ("Warp", "Kaleidoscope") and not palette and st.get("T_CHECKBOX_Canvas") != "1":
        warn(f"{tag}: {effect} needs T_CHECKBOX_Canvas=1 to affect lower layers")


# --------------------------------------------------------------------------- CLI

def cmd_info(a):
    seq = Sequence.load(a.file)
    print(f"File: {a.file}")
    print(f"Version {seq.head('version')} | {seq.head('sequenceType')} | {seq.frame_ms} ms frames "
          f"({1000 // seq.frame_ms if seq.frame_ms else '?'} fps) | {seq.duration_ms / 1000:.3f} s")
    for t in ("mediaFile", "song", "artist", "author", "comment"):
        if seq.head(t):
            print(f"{t}: {seq.head(t)}")
    print(f"EffectDB: {len(seq.effect_strings())} entries, ColorPalettes: {len(seq.palette_strings())}")
    for el in seq.section("ElementEffects").findall("Element"):
        if el.get("type") == "timing":
            ls = el.findall("EffectLayer")
            marks = [len(l.findall("Effect")) for l in ls]
            fx = f" fixed {el.get('fixed')} ms" if el.get("fixed") else ""
            print(f"[timing] {el.get('name')}: {len(ls)} layer(s), marks {marks}{fx}")
    cur = None
    for fx in seq.iter_effects():
        if fx["model"] != cur:
            cur = fx["model"]
            print(f"[model] {cur}")
        where = f"{fx['sub']} " if fx["sub"] else ""
        pal = [fx["palette"].get(f"C_BUTTON_Palette{i}") for i in range(1, 9)
               if fx["palette"].get(f"C_CHECKBOX_Palette{i}") == "1"]
        print(f"   {where}L{fx['layer']} {fx['start']:>7}-{fx['end']:<7} {fx['name']:<14} colors={pal}")
        if a.verbose:
            for k, v in fx["settings"].items():
                print(f"        {k}={v}")


def cmd_validate(a):
    issues = validate(a.file, a.show)
    for lvl, m in issues:
        print(f"{lvl}: {m}")
    errs = sum(1 for l, _ in issues if l == "ERROR")
    print(f"{errs} error(s), {len(issues) - errs} warning(s)")
    return 1 if errs else 0


def cmd_layout(a):
    lay = load_layout(a.show)
    print(f"Layout: {lay['path']}")
    print(f"Models ({len(lay['models'])}):")
    keys = ("NumStrings", "NodesPerString", "StrandsPerString", "NumArches", "NodesPerArch", "NumCanes",
            "NodesPerCane", "parm1", "parm2", "parm3", "CustomWidth", "CustomHeight", "StringType",
            "StartChannel", "Controller")
    for n, m in sorted(lay["models"].items()):
        info = ", ".join(f"{k}={m['attrs'][k]}" for k in keys if k in m["attrs"])
        print(f"  {n} [{m['type']}] {info}")
        for lbl in ("submodels", "faces", "states", "aliases"):
            if m[lbl]:
                print(f"      {lbl}: {', '.join(m[lbl])}")
    print(f"Groups ({len(lay['groups'])}):")
    for n, g in sorted(lay["groups"].items()):
        print(f"  {n} [layout={g['layout']}]: {', '.join(g['models'])}")


def cmd_effect(a):
    name, e = find_effect(a.name)
    print(f"{name}  (reference: {e['file']})")
    if e.get("canvasMode"):
        print("  canvas effect: T_CHECKBOX_Canvas=1")
    for t in e["tabs"]:
        print(f"  {t['key']} = {' | '.join(t['options'])}  (default {t['default']})")
    for p in e["properties"]:
        if p.get("custom"):
            continue
        rng = " | ".join(p["options"]) if isinstance(p.get("options"), list) else \
            (f"{p['valueMin']:g}..{p['valueMax']:g}" if "valueMin" in p else
             (f"{p.get('min')}..{p.get('max')}" if "min" in p else ""))
        if p.get("dynamicOptions"):
            rng += f" <{p['dynamicOptions']}>"
        vc = " [VC]" if "valueCurve" in p else ""
        print(f"  {p['key']} = {p.get('default')!s:<10} {rng}{vc}")
        if a.all and p.get("description"):
            print(f"      {p['description']}")
    if a.all:
        print("Shared keys: see references/effect-settings.md")


def cmd_new(a):
    out = Path(a.out)
    if out.exists() and not a.force:
        print(f"{out} exists; use --force to overwrite", file=sys.stderr)
        return 1
    seq = Sequence.new(a.duration, a.frame_ms, a.media or "", song=a.song or "", artist=a.artist or "")
    for m in (a.models.split(",") if a.models else []):
        if m.strip():
            seq.add_model(m.strip())
    seq.save(out)
    print(f"Created {out}")


def cmd_add_effect(a):
    seq = Sequence.load(a.file)
    st = {}
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        st[k] = v
    colors = [c for c in a.colors.split(",")] if a.colors else None
    seq.add_effect(a.model, a.effect, a.start, a.end, layer=a.layer, settings=st, colors=colors,
                   submodel=a.submodel)
    seq.save(backup=not a.no_backup)
    print(f"Added {a.effect} to {a.model} layer {a.layer} {a.start}-{a.end}")


def cmd_add_timing(a):
    seq = Sequence.load(a.file)
    if a.xtiming:
        x = ET.parse(a.xtiming).getroot()
        tims = [x] if x.tag == "timing" else x.findall("timing")
        for t in tims:
            layers = [[(int(e.get("starttime")), int(e.get("endtime")), e.get("label", ""))
                       for e in l.findall("Effect")] for l in t.findall("EffectLayer")]
            seq.add_timing(a.name or t.get("name"), layers=layers)
    elif a.fixed:
        seq.add_timing(a.name, fixed=a.fixed)
    else:
        seq.add_timing(a.name, marks=[int(x) for x in a.marks.split(",")])
    seq.save(backup=not a.no_backup)
    print("Timing track added")


def build_color_test(models, colors, hold_s=4.0, frame_ms=50):
    """Sequence that shows each colour at full for `hold_s`, then fades it 100->0 % over
    `hold_s`, on every model at once. A 'Swatches' timing track labels each step."""
    hold = int(round(hold_s * 1000 / frame_ms)) * frame_ms
    seq = Sequence.new(duration_s=len(colors) * 2 * hold / 1000, frame_ms=frame_ms,
                       comment="Colour test: full then fade for each swatch")
    marks = []
    for i, c in enumerate(colors):
        t = i * 2 * hold
        marks += [(t, t + hold, f"{c} full"), (t + hold, t + 2 * hold, f"{c} fade")]
    seq.add_timing("Swatches", marks=marks)
    for m in models:
        seq.add_model(m)
        for i, c in enumerate(colors):
            t = i * 2 * hold
            seq.add_effect(m, "On", t, t + hold, colors=[c])
            seq.add_effect(m, "On", t + hold, t + 2 * hold, colors=[c],
                           settings={"E_TEXTCTRL_Eff_On_Start": "100", "E_TEXTCTRL_Eff_On_End": "0"})
    return seq


def cmd_color_test(a):
    out = Path(a.out)
    if out.exists() and not a.force:
        print(f"{out} exists; use --force to overwrite", file=sys.stderr)
        return 1
    if a.models:
        models = [m.strip() for m in a.models.split(",") if m.strip()]
    else:
        models = sorted(load_layout(a.show)["models"]) if a.show else []
    if not models:
        print("give --models or --show", file=sys.stderr)
        return 1
    colors = [c.strip() for c in a.colors.split(",")]
    seq = build_color_test(models, colors, a.hold, a.frame_ms)
    seq.save(out)
    print(f"Created {out}: {len(colors)} swatches x {a.hold:g}s full + {a.hold:g}s fade on {len(models)} model(s)")


def cmd_vc(a):
    ps = [float(x) for x in a.params]
    k, v = value_curve(a.effect, a.prop, a.type, *ps)
    print(f"{k}={v}")


def find_xlights():
    for p in ("/Applications/xLights.app/Contents/MacOS/xLights",
              r"C:\Program Files\xLights\xLights.exe",
              "/usr/bin/xLights", "/usr/local/bin/xLights", "/opt/xLights/xLights"):
        if Path(p).exists():
            return p
    return shutil.which("xLights")


def cmd_render(a):
    exe = a.xlights or find_xlights()
    if not exe:
        print("xLights binary not found; pass --xlights PATH", file=sys.stderr)
        return 2
    cmd = [exe, "--headless", "-s", str(Path(a.show).resolve()), str(Path(a.file).resolve())]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd)
    print(f"exit code {r.returncode} (0 = rendered OK)")
    return r.returncode


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("info"); p.add_argument("file"); p.add_argument("-v", "--verbose", action="store_true")
    p.set_defaults(fn=cmd_info)
    p = sub.add_parser("validate"); p.add_argument("file"); p.add_argument("--show")
    p.set_defaults(fn=cmd_validate)
    p = sub.add_parser("layout"); p.add_argument("show"); p.set_defaults(fn=cmd_layout)
    p = sub.add_parser("effect"); p.add_argument("name"); p.add_argument("--all", action="store_true")
    p.set_defaults(fn=cmd_effect)
    p = sub.add_parser("new"); p.add_argument("out"); p.add_argument("--duration", type=float, required=True)
    p.add_argument("--frame-ms", type=int, default=50); p.add_argument("--media")
    p.add_argument("--models"); p.add_argument("--song"); p.add_argument("--artist")
    p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_new)
    p = sub.add_parser("add-effect"); p.add_argument("file"); p.add_argument("--model", required=True)
    p.add_argument("--effect", required=True); p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True); p.add_argument("--layer", type=int, default=0)
    p.add_argument("--submodel"); p.add_argument("--set", action="append")
    p.add_argument("--colors"); p.add_argument("--no-backup", action="store_true")
    p.set_defaults(fn=cmd_add_effect)
    p = sub.add_parser("add-timing"); p.add_argument("file"); p.add_argument("--name")
    p.add_argument("--marks"); p.add_argument("--fixed", type=int); p.add_argument("--xtiming")
    p.add_argument("--no-backup", action="store_true"); p.set_defaults(fn=cmd_add_timing)
    p = sub.add_parser("color-test"); p.add_argument("out"); p.add_argument("--colors", required=True)
    p.add_argument("--show"); p.add_argument("--models"); p.add_argument("--hold", type=float, default=4.0)
    p.add_argument("--frame-ms", type=int, default=50); p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_color_test)
    p = sub.add_parser("vc"); p.add_argument("effect"); p.add_argument("prop"); p.add_argument("type")
    p.add_argument("params", nargs="*"); p.set_defaults(fn=cmd_vc)
    p = sub.add_parser("render"); p.add_argument("file"); p.add_argument("--show", required=True)
    p.add_argument("--xlights"); p.set_defaults(fn=cmd_render)
    a = ap.parse_args(argv)
    try:
        return a.fn(a) or 0
    except (KeyError, ValueError) as ex:
        print(f"error: {ex}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
