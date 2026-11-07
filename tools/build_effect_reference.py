#!/usr/bin/env python3
"""Regenerate the bundled xLights effect reference from an xLights source checkout.

Reads resources/effectmetadata/*.json (the same metadata the desktop and iPad
effect panels are built from) and writes:

  skills/xlights/data/effects.json          machine-readable key/range/default table
  skills/xlights/references/effects/*.md    one human-readable page per effect
  skills/xlights/references/effects/README.md  index of all effects

Usage:
  python3 tools/build_effect_reference.py /path/to/xLights [--ref 2026.19]

--ref names the xLights release (tag) the checkout is at; it is recorded in the output so CI and
maintainers know which stable release the reference describes. Use the latest stable release
(tools/latest_xlights_release.sh), not master.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "xlights"

CONTROL_PREFIX = {
    "checkbox": "CHECKBOX",
    "togglebutton": "CHECKBOX",
    "choice": "CHOICE",
    "combobox": "CHOICE",
    "spin": "SPINCTRL",
    "text": "TEXTCTRL",
    # desktop JsonEffectPanel names these ID_FILEPICKERCTRL_ / ID_COLOURPICKERCTRL_
    "filepicker": "FILEPICKERCTRL",
    "fontpicker": "FONTPICKER",
    "colourpicker": "COLOURPICKERCTRL",
}

# Keys behind per-effect "custom" controls, taken from each effect's render code
# (src-core/effects/<Name>Effect.cpp). Merged into the generated tables.
EXTRA_EFFECT_KEYS = {
    "Faces": [
        {"key": "E_CHOICE_Faces_TimingTrack", "type": "enum", "default": "", "dynamicOptions": "lyricTimingTracks",
         "description": "Lip-sync source: name of a lyric timing track (its 3rd layer holds phonemes). Leave empty and set E_CHOICE_Faces_Phoneme for a fixed mouth."},
        {"key": "E_CHOICE_Faces_Phoneme", "type": "enum", "default": "",
         "options": ["AI", "E", "etc", "FV", "L", "MBP", "O", "rest", "U", "WQ"],
         "description": "Fixed mouth shape used when no timing track is selected."},
        {"key": "E_CHECKBOX_Faces_TransparentBlack", "type": "bool", "default": 0,
         "description": "Matrix faces: key out dark image pixels."},
        {"key": "E_TEXTCTRL_Faces_TransparentBlack", "type": "int", "default": 0, "min": 0, "max": 300,
         "description": "Transparent-black brightness threshold."},
    ],
    "State": [
        {"key": "E_CHOICE_State_State", "type": "enum", "default": "", "dynamicOptions": "states",
         "description": "State name to show (when driving states directly). Leave empty and set E_CHOICE_State_TimingTrack to drive from timing labels."},
        {"key": "E_CHOICE_State_TimingTrack", "type": "enum", "default": "", "dynamicOptions": "timingTracks",
         "description": "Timing track whose mark labels name the state to show at each mark."},
    ],
    "Pictures": [
        {"key": "E_TEXTCTRL_Pictures_Filename", "type": "file", "default": "",
         "description": "Image/GIF path (relative to the show folder is best)."},
        {"key": "E_CHECKBOX_Pictures_TransparentBlack", "type": "bool", "default": 0, "description": "Key out dark pixels."},
        {"key": "E_TEXTCTRL_Pictures_TransparentBlack", "type": "int", "default": 0, "min": 0, "max": 300,
         "description": "Transparent-black brightness threshold."},
    ],
    "Video": [
        {"key": "E_FILEPICKERCTRL_Video_Filename", "type": "file", "default": "",
         "description": "Video file path (relative to the show folder is best)."},
        {"key": "E_CHECKBOX_Video_TransparentBlack", "type": "bool", "default": 0, "description": "Key out dark pixels."},
        {"key": "E_TEXTCTRL_Video_TransparentBlack", "type": "int", "default": 0, "min": 0, "max": 300,
         "description": "Transparent-black brightness threshold."},
    ],
    "Text": [
        {"key": "E_FILEPICKERCTRL_Text_File", "type": "file", "default": "",
         "description": "Text file to display instead of E_TEXTCTRL_Text."},
        {"key": "E_CHOICE_Text_Font", "type": "enum", "default": "Use OS Fonts", "dynamicOptions": "xlFonts",
         "description": "xLights bitmap font, or 'Use OS Fonts' to use E_FONTPICKER_Text_Font."},
    ],
    "Shape": [
        {"key": "E_FILEPICKERCTRL_SVG", "type": "file", "default": "", "description": "SVG used when Object to Draw = SVG."},
        {"key": "E_FONTPICKER_Shape_Font", "type": "font", "default": "", "description": "Font for Emoji objects."},
        {"key": "E_SPINCTRL_Shape_Char", "type": "int", "default": 127876, "description": "Unicode code point for Emoji objects."},
        {"key": "E_CHOICE_Shape_SkinTone", "type": "enum", "default": "", "description": "Emoji skin tone."},
    ],
    "Ripple": [
        {"key": "E_FILEPICKERCTRL_Ripple_SVG", "type": "file", "default": "", "description": "SVG used when Object to Draw = SVG."},
    ],
    "Servo": [
        {"key": "E_TEXTCTRL_Servo", "type": "float", "default": "0.0", "description": "Start position 0.0-100.0 %.",
         "valueCurve": "E_VALUECURVE_Servo"},
        {"key": "E_TEXTCTRL_EndValue", "type": "float", "default": "0.0", "description": "End position 0.0-100.0 %."},
        {"key": "E_TOGGLEBUTTON_Start", "type": "bool", "default": 0, "description": "Link toggle (UI)."},
        {"key": "E_TOGGLEBUTTON_End", "type": "bool", "default": 0, "description": "Link toggle (UI)."},
    ],
    "DMX": [
        {"key": f"E_SLIDER_DMX{n}", "type": "int", "default": 0, "min": 0, "max": 255,
         "valueCurve": f"E_VALUECURVE_DMX{n}", "description": f"DMX channel {n} value."} for n in range(1, 49)
    ] + [
        {"key": f"E_CHECKBOX_INVDMX{n}", "type": "bool", "default": 0, "description": f"Invert DMX channel {n}."}
        for n in range(1, 49)
    ],
}

# Keys written by bespoke ("custom") controls on the shared panels. They are not
# derivable from the metadata, so they are listed here from the render code
# (src-core/render/PixelBuffer.cpp, ColorPanel/BlendingPanel/BufferPanel).
SHARED_CUSTOM_KEYS = {
    "Color": [
        {"key": f"C_BUTTON_Palette{i}", "type": "color",
         "default": d, "description": f"Palette slot {i} colour (#rrggbb) or an active colour curve string."}
        for i, d in enumerate(["#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
                               "#FFFF00", "#000000", "#00FFFF", "#FF00FF"], 1)
    ] + [
        {"key": f"C_CHECKBOX_Palette{i}", "type": "bool", "default": 1 if i <= 2 else 0,
         "description": f"1 = palette slot {i} is enabled (used by the effect)."}
        for i in range(1, 9)
    ] + [
        {"key": "C_CHECKBOXBRIGHTNESSLEVEL", "type": "bool", "default": 0,
         "description": "Brightness Level: scale brightness by the colour's value. Note: no underscore after CHECKBOX."},
        {"key": "C_CHECKBOX_Chroma", "type": "bool", "default": 0, "description": "Enable chroma key."},
        {"key": "C_SLIDER_ChromaSensitivity", "type": "int", "default": 1, "min": 1, "max": 255,
         "description": "Chroma key sensitivity."},
        {"key": "C_COLOURPICKERCTRL_ChromaColour", "type": "color", "default": "#000000",
         "description": "Chroma key colour."},
        {"key": "C_SLIDER_SparkleFrequency", "type": "int", "default": 0, "min": 0, "max": 200,
         "valueCurve": "C_VALUECURVE_SparkleFrequency",
         "description": "Sparkles: 0 = off; higher = more random white/colour sparkles over the effect."},
        {"key": "C_CHECKBOX_MusicSparkles", "type": "bool", "default": 0,
         "description": "Sparkle frequency follows the music intensity."},
        {"key": "C_COLOURPICKERCTRL_SparklesColour", "type": "color", "default": "#FFFFFF",
         "description": "Colour of sparkles."},
    ],
    "Blending": [
        {"key": "T_CHOICE_LayerMethod", "type": "enum", "default": "Normal",
         "options": ["Normal", "Effect 1", "Effect 2", "1 is Mask", "2 is Mask", "1 is Unmask",
                     "2 is Unmask", "1 is True Unmask", "2 is True Unmask", "1 reveals 2",
                     "2 reveals 1", "Shadow 1 on 2", "Shadow 2 on 1", "Layered", "Average",
                     "Bottom-Top", "Left-Right", "Highlight", "Highlight Vibrant", "Additive",
                     "Subtractive", "Brightness", "Max", "Min"],
         "description": "How this layer (\"1\") mixes onto the composite of the layers below it (\"2\"). Ignored on the bottom-most active layer."},
        {"key": "T_SLIDER_EffectLayerMix", "type": "int", "default": 0, "min": 0, "max": 100,
         "valueCurve": "T_VALUECURVE_EffectLayerMix",
         "description": "Mix amount / threshold used by the layer method (0-100)."},
        {"key": "T_CHECKBOX_LayerMorph", "type": "bool", "default": 0,
         "description": "Morph: cross-fade the mix from layer 1 to layer 2 across the effect duration."},
        {"key": "T_CHECKBOX_Canvas", "type": "bool", "default": 0,
         "description": "Canvas mode: this effect draws on top of (and can read) the layers below it. Needed by Warp, Kaleidoscope, etc."},
        {"key": "T_LayersSelected", "type": "string", "default": "",
         "description": "Canvas mode: which lower layers feed this layer (set by the Layers... dialog)."},
        {"key": "T_CHOICE_In_Transition_Type", "type": "enum", "default": "Fade",
         "options": ["Blend", "Blinds", "Blobs", "Bow Tie", "Circle Explode", "Circles", "Circular Swirl",
                     "Clock", "Dissolve", "Doorway", "Fade", "Fold", "From Middle", "Pinwheel", "Shatter",
                     "Slide Bars", "Slide Checks", "Square Explode", "Star", "Swap", "Wipe", "Zoom"],
         "description": "In transition style. Only applies when T_TEXTCTRL_Fadein > 0."},
        {"key": "T_TEXTCTRL_Fadein", "type": "float", "default": "0.00",
         "description": "In transition time in SECONDS (e.g. 0.50)."},
        {"key": "T_CHOICE_Out_Transition_Type", "type": "enum", "default": "Fade",
         "options": "same as T_CHOICE_In_Transition_Type",
         "description": "Out transition style. Only applies when T_TEXTCTRL_Fadeout > 0."},
        {"key": "T_TEXTCTRL_Fadeout", "type": "float", "default": "0.00",
         "description": "Out transition time in SECONDS."},
    ],
    "Buffer": [
        {"key": "B_CUSTOM_SubBuffer", "type": "string", "default": "",
         "description": "Sub-buffer rectangle as percentages 'x1xy1xx2xy2' style string written by the UI; leave unset for full buffer. Easiest to set in xLights."},
    ],
}


def control_prefix(prop):
    sp = prop.get("settingPrefix")
    if sp:
        return sp
    ct = prop["controlType"]
    if ct == "slider":
        return "TEXTCTRL" if prop.get("divisor", 1) > 1 else "SLIDER"
    return CONTROL_PREFIX.get(ct, "TEXTCTRL")


def encoding_note(prop, cp):
    div = prop.get("divisor", 1)
    if prop["type"] == "float" and div > 1:
        decimals = len(str(div)) - 1
        if cp == "SLIDER":
            return f"raw int = value x {div} (e.g. 1.0 -> {div})"
        return f"float text with {decimals} decimal(s) (e.g. {1:.{decimals}f})"
    return ""


def fmt_default(prop, cp):
    d = prop.get("default")
    div = prop.get("divisor", 1)
    if isinstance(d, bool):
        return 1 if d else 0
    if prop["type"] == "float" and div > 1 and isinstance(d, (int, float)):
        if cp == "SLIDER":
            return int(round(d * div))
        return f"{float(d):.{len(str(div)) - 1}f}"
    return d


def build_props(meta, prefix):
    out = []
    for p in meta.get("properties", []):
        if p.get("platform") == "ipad":
            continue
        if p["controlType"] == "custom":
            out.append({"id": p["id"], "custom": True, "description": p.get("description", "")})
            continue
        cp = control_prefix(p)
        if p["controlType"] == "point2d":
            for axis in ("X", "Y"):
                entry = {
                    "id": p["id"] + axis,
                    "key": f"{prefix}{cp}_{p['id']}{axis}",
                    "label": f"{p.get('label', '')} {axis}",
                    "type": p["type"],
                    "default": p.get("default" + axis, p.get("default")),
                    "min": p.get("min" + axis, p.get("min")),
                    "max": p.get("max" + axis, p.get("max")),
                    "description": p.get("description", ""),
                }
                if p.get("valueCurve"):
                    entry["valueCurve"] = f"{prefix}VALUECURVE_{p['id']}{axis}"
                out.append(entry)
            continue
        entry = {
            "id": p["id"],
            "key": f"{prefix}{cp}_{p['id']}",
            "label": p.get("label", ""),
            "type": p["type"],
            "default": fmt_default(p, cp),
            "description": p.get("description", ""),
        }
        for k in ("min", "max", "divisor", "vcMin", "vcMax", "options", "dynamicOptions"):
            if k in p:
                entry[k] = p[k]
        enc = encoding_note(p, cp)
        if enc:
            entry["encoding"] = enc
        div = p.get("divisor", 1)
        if div > 1 and "min" in p and "max" in p:
            # min/max (and value-curve Min/Max) are in raw slider units; these are the real values
            entry["valueMin"] = p["min"] / div
            entry["valueMax"] = p["max"] / div
        if p.get("valueCurve"):
            entry["valueCurve"] = f"{prefix}VALUECURVE_{p['id']}"
        if p.get("suppressIfDefault"):
            entry["omitIfDefault"] = True
        out.append(entry)
    return out


def build_tabs(meta, props_by_id):
    tabs = []
    for g in meta.get("groups", []) or []:
        if g.get("type") == "tabs" and g.get("settingKey"):
            tabs.append({
                "key": g["settingKey"],
                "options": [t["label"] for t in g.get("tabs", [])],
                "default": g["tabs"][0]["label"] if g.get("tabs") else "",
                "tabs": {t["label"]: [props_by_id[i]["key"] for i in t.get("properties", [])
                                      if i in props_by_id and "key" in props_by_id[i]]
                         for t in g.get("tabs", [])},
            })
    return tabs


def cond_text(w):
    if "allOf" in w:
        return " AND ".join(cond_text(x) for x in w["allOf"])
    if "any" in w:
        # "any" lists checkbox ids: true when any of them is checked
        return " OR ".join((x + " checked") if isinstance(x, str) else cond_text(x) for x in w["any"])
    prop = w.get("property", "?")
    for k, op in (("equals", "=="), ("notEquals", "!="), ("oneOf", "in"), ("notOneOf", "not in"),
                  ("startsWith", "starts with")):
        if k in w:
            return f"{prop} {op} {w[k]!r}"
    return prop


def rules_text(meta):
    lines = []
    for r in meta.get("visibilityRules", []) or []:
        acts = "; ".join(f"{k} {', '.join(v) if isinstance(v, list) else v}" for k, v in r.items() if k != "when")
        lines.append(f"- when `{cond_text(r.get('when', {}))}`: {acts}")
    return lines


def md_cell(v):
    s = "" if v is None else str(v)
    return s.replace("|", "\\|").replace("\n", " ")


def write_effect_md(name, meta, entry, path):
    lines = [f"# {name} effect", ""]
    if meta.get("description"):
        lines += [meta["description"].strip(), ""]
    lines += [f'XML: `<Effect name="{name}" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.', ""]
    if meta.get("canvasMode"):
        lines += ["**Canvas effect**: set `T_CHECKBOX_Canvas=1`; it transforms the layers below it.", ""]
    if entry["tabs"]:
        lines += ["## Mode tabs", ""]
        for t in entry["tabs"]:
            lines.append(f"- `{t['key']}` = one of {', '.join(repr(o) for o in t['options'])} (default {t['default']!r}).")
            for label, keys in t["tabs"].items():
                if keys:
                    lines.append(f"  - {label}: {', '.join('`'+k+'`' for k in keys)}")
        lines.append("")
    lines += ["## Settings", "", "| Key | Type | Default | Range / options | Notes |", "|---|---|---|---|---|"]
    for p in entry["properties"]:
        if p.get("custom"):
            continue
        rng = ""
        if "options" in p:
            rng = ", ".join(p["options"])
        elif "valueMin" in p:
            rng = f"{p['valueMin']:g} .. {p['valueMax']:g} (raw {p['min']} .. {p['max']}, divisor {p['divisor']})"
        elif "min" in p or "max" in p:
            rng = f"{p.get('min')} .. {p.get('max')}"
        if p.get("dynamicOptions"):
            rng = (rng + " " if rng else "") + f"(dynamic: {p['dynamicOptions']})"
        notes = p.get("description", "")
        if p.get("encoding"):
            notes = f"[{p['encoding']}] " + notes
        if p.get("valueCurve"):
            notes = f"[VC: `{p['valueCurve']}`] " + notes
        lines.append(f"| `{p['key']}` | {p['type']} | {md_cell(p.get('default'))} | {md_cell(rng)} | {md_cell(notes)} |")
    customs = [p for p in entry["properties"] if p.get("custom")]
    if customs:
        lines += ["", "## Custom controls (set these in the xLights UI if possible)", ""]
        for p in customs:
            lines.append(f"- `{p['id']}`: {md_cell(p['description'])}")
    rt = rules_text(meta)
    if rt:
        lines += ["", "## Visibility rules (which settings matter when)", ""] + rt
    if meta.get("notes"):
        lines += ["", "## Notes", ""] + [f"- {n}" for n in meta["notes"]]
    path.write_text("\n".join(lines) + "\n")


def main():
    args = sys.argv[1:]
    ref = ""
    if "--ref" in args:
        i = args.index("--ref")
        ref = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    xl = Path(args[0])
    md_dir = xl / "resources" / "effectmetadata"
    try:
        commit = subprocess.run(["git", "-C", str(xl), "log", "-1", "--format=%h %cd", "--date=short"],
                                capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        commit = "unknown"
    try:
        full_sha = subprocess.run(["git", "-C", str(xl), "rev-parse", "HEAD"],
                                  capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        full_sha = ""

    out_dir = SKILL / "references" / "effects"
    out_dir.mkdir(parents=True, exist_ok=True)
    (SKILL / "data").mkdir(parents=True, exist_ok=True)

    label = f"{ref} ({commit})" if ref else commit
    result = {"_source": f"xLights resources/effectmetadata @ {label}", "_release": ref, "_commit": full_sha,
              "effects": {}, "shared": {}}
    index_rows = []

    for f in sorted(md_dir.glob("*.json")):
        if f.name.startswith("_"):
            continue
        meta = json.loads(f.read_text())
        name = meta["effectName"]
        props = build_props(meta, "E_")
        for extra in EXTRA_EFFECT_KEYS.get(name, []):
            props.append(dict(extra, id=extra["key"].split("_", 2)[2], extra=True))
        by_id = {p["id"]: p for p in props}
        entry = {"file": f"references/effects/{f.stem}.md", "properties": props, "tabs": build_tabs(meta, by_id)}
        if meta.get("canvasMode"):
            entry["canvasMode"] = True
        result["effects"][name] = entry
        write_effect_md(name, meta, entry, out_dir / f"{f.stem}.md")
        index_rows.append((name, f.stem, (meta.get("description") or "").split("\n")[0]))

    for f in sorted((md_dir / "shared").glob("*.json")):
        meta = json.loads(f.read_text())
        prefix = meta.get("prefix", "E_")
        props = build_props(meta, prefix)
        props += SHARED_CUSTOM_KEYS.get(meta["effectName"], [])
        result["shared"][meta["effectName"]] = {"prefix": prefix, "properties": props,
                                                "notes": meta.get("notes", [])}

    (SKILL / "data" / "effects.json").write_text(json.dumps(result, indent=1) + "\n")

    idx = ["# Effect reference index", "",
           f"Generated from xLights {'release ' + ref + ' ' if ref else ''}`resources/effectmetadata` ({commit}) by `tools/build_effect_reference.py`.",
           "Each page lists every setting key, its type, default, range/options and what it does.",
           "Machine-readable version: `data/effects.json`.", "",
           "| Effect (XML name) | Page |", "|---|---|"]
    for name, stem, _ in index_rows:
        idx.append(f"| `{name}` | [{stem}.md]({stem}.md) |")
    (out_dir / "README.md").write_text("\n".join(idx) + "\n")
    print(f"Wrote {len(index_rows)} effects from {label}")


if __name__ == "__main__":
    main()
