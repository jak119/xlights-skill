#!/usr/bin/env python3
"""Self-tests for the xLights skill.

  python3 tests/test_skill.py            offline tests (no xLights needed)
  XLIGHTS_BIN=/path/to/xLights XLIGHTS_SHOW=/path/to/a/show python3 tests/test_skill.py
                                         + integration tests that headless-render with real xLights

Integration tests write only files named "zz skilltest *" into XLIGHTS_SHOW and delete them afterwards.
On macOS the show folder must be one xLights has opened before (sandbox bookmark).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "xlights"
FIX = ROOT / "tests" / "fixtures" / "show"
sys.path.insert(0, str(SKILL / "scripts"))

import xsq  # noqa: E402


def all_known_keys():
    d = json.loads((SKILL / "data" / "effects.json").read_text())
    known = set()
    for e in d["effects"].values():
        known.update(t["key"] for t in e["tabs"])
        for p in e["properties"]:
            known.update(k for k in (p.get("key"), p.get("valueCurve")) if k)
    for s in d["shared"].values():
        for p in s["properties"]:
            known.update(k for k in (p.get("key"), p.get("valueCurve")) if k)
    return known


class TestReferenceData(unittest.TestCase):
    def test_every_fixture_key_is_known(self):
        """Keys xLights actually wrote must all be predicted by effects.json."""
        known = all_known_keys()
        for f in FIX.glob("*.xsq"):
            root = ET.parse(f).getroot()
            for n in list(root.iter("Effect")) + list(root.iter("ColorPalette")):
                if n.text and "=" in n.text:
                    for k in xsq.decode_settings(n.text):
                        self.assertIn(k, known, f"{f.name}: {k}")

    def test_extra_key_dirs(self):
        """Set XLIGHTS_SKILL_EXTRA_SHOWS=dir1:dir2 to check more real sequences (e.g. your own shows)."""
        dirs = [d for d in os.environ.get("XLIGHTS_SKILL_EXTRA_SHOWS", "").split(os.pathsep) if d]
        if not dirs:
            self.skipTest("XLIGHTS_SKILL_EXTRA_SHOWS not set")
        known = all_known_keys()
        missing = {}
        for d in dirs:
            for f in Path(d).glob("*.xsq"):
                root = ET.parse(f).getroot()
                for n in list(root.iter("Effect")) + list(root.iter("ColorPalette")):
                    if n.text and "=" in n.text:
                        for k in xsq.decode_settings(n.text):
                            if k not in known:
                                missing.setdefault(k, f.name)
        self.assertEqual(missing, {}, "keys not in effects.json")

    def test_generated_from_stable_release(self):
        """The reference must describe a published release (YYYY.N[.N]), never master/nightly."""
        d = json.loads((SKILL / "data" / "effects.json").read_text())
        self.assertRegex(d.get("_release", ""), r"^\d{4}\.\d+(\.\d+)?$")
        self.assertRegex(d.get("_commit", ""), r"^[0-9a-f]{40}$")

    def test_every_effect_has_a_page(self):
        d = json.loads((SKILL / "data" / "effects.json").read_text())
        self.assertGreaterEqual(len(d["effects"]), 50)
        for name, e in d["effects"].items():
            self.assertTrue((SKILL / e["file"]).exists(), name)

    def test_reference_links_resolve(self):
        """Every references/*.md mentioned in SKILL.md exists."""
        text = (SKILL / "SKILL.md").read_text()
        for ref in set(re.findall(r"references/[\w\-/<>.]+\.md", text)):
            if "<" in ref:
                continue
            self.assertTrue((SKILL / ref).exists(), ref)

    def test_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text()
        m = re.match(r"---\nname: (\S+)\ndescription: (.+?)\n---\n", text, re.S)
        self.assertIsNotNone(m, "SKILL.md frontmatter")
        self.assertEqual(m.group(1), SKILL.name)
        self.assertLess(len(m.group(2)), 1024)


class TestValidator(unittest.TestCase):
    def test_fixtures_have_no_errors(self):
        for f in FIX.glob("*.xsq"):
            errs = [m for lvl, m in xsq.validate(f, FIX) if lvl == "ERROR"]
            self.assertEqual(errs, [], f.name)

    def test_alias_is_warned(self):
        msgs = [m for _, m in xsq.validate(FIX / "Layered.xsq", FIX)]
        self.assertTrue(any("alias" in m for m in msgs))

    def test_detects_problems(self):
        seq = xsq.Sequence.new(10)
        seq.add_model("Not A Model")
        seq.add_effect("Not A Model", "Bars", 0, 1000, settings={"E_SLIDER_Bars_Typo": "1",
                                                              "E_CHOICE_SingleStrand_TimingTrack": "x"})
        # force an overlap and a bad ref by hand
        layer = seq.root.find("ElementEffects/Element/EffectLayer")
        ET.SubElement(layer, "Effect", {"ref": "99", "name": "On", "startTime": "500", "endTime": "1500",
                                        "palette": "0"})
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.xsq"
            seq.save(p, backup=False)
            msgs = " | ".join(m for _, m in xsq.validate(p, FIX))
        for needle in ("not in layout", "ref=99", "overlapping", "E_SLIDER_Bars_Typo"):
            self.assertIn(needle, msgs)


class TestBuilder(unittest.TestCase):
    def test_build_and_round_trip(self):
        seq = xsq.Sequence.new(20, frame_ms=50)
        seq.add_timing("Beats", marks=list(range(0, 20001, 500)))
        seq.add_timing("Grid", fixed=1000)
        seq.add_timing("Lyrics", layers=[[(0, 1000, "Hi there")], [(0, 500, "Hi"), (500, 1000, "there")],
                                         [(0, 250, "AI"), (250, 500, "rest")]])
        seq.add_model("All Lines")
        seq.add_effect("Single Line", "colorwash", 0, 20000, layer=1, colors=["#FF6600"])
        seq.add_effect("Single Line", "Text", 0, 5000, settings={"E_TEXTCTRL_Text": "Merry, Xmas & joy"})
        seq.add_effect("Single Line", "On", 0, 500, submodel="Left Half")
        seq.add_effect("Single Line-2", "SingleStrand", 0, 20000,
                       settings={"E_CHOICE_SingleStrand_TimingTrack": "Beats"})
        with self.assertRaises(ValueError):
            seq.add_effect("Single Line", "On", 4000, 6000)  # overlaps Text
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "built.xsq"
            seq.save(p, backup=False)
            self.assertEqual([m for l, m in xsq.validate(p, FIX) if l == "ERROR"], [])
            raw = p.read_text()
            self.assertIn("Merry&amp;comma; Xmas &amp;amp; joy", raw)
            again = xsq.Sequence.load(p)
            texts = [f["settings"]["E_TEXTCTRL_Text"] for f in again.iter_effects() if f["name"] == "Text"]
            self.assertEqual(texts, ["Merry, Xmas & joy"])
            tags = [c.tag for c in again.root]
            self.assertLess(tags.index("EffectDB"), tags.index("ElementEffects"))
            self.assertLess(tags.index("DisplayElements"), tags.index("ElementEffects"))

    def test_load_save_preserves_xlights_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "t.xsq"
            xsq.Sequence.load(FIX / "Testing.xsq").save(p, backup=False)
            a, b = ET.parse(FIX / "Testing.xsq").getroot(), ET.parse(p).getroot()
            self.assertEqual([c.tag for c in a], [c.tag for c in b])
            self.assertEqual(len(list(a.iter())), len(list(b.iter())))

    def test_update_effect_in_place(self):
        """Edit the Chase on Single Line in an xLights-written file without touching shared entries."""
        seq = xsq.Sequence.load(FIX / "Testing.xsq")
        before = {f["model"]: dict(f["settings"]) for f in seq.iter_effects()}
        fx = next(f for f in seq.iter_effects() if f["model"] == "Single Line")
        seq.update_effect(fx["node"], settings={"E_CHOICE_Chase_Type1": "Right-Left",
                                                "T_TEXTCTRL_Fadeout": "1.00"})
        after = {f["model"]: f["settings"] for f in seq.iter_effects()}
        self.assertEqual(after["Single Line"]["E_CHOICE_Chase_Type1"], "Right-Left")
        self.assertEqual(after["Single Line"]["T_TEXTCTRL_Fadeout"], "1.00")
        self.assertEqual(after["Single Line-2"], before["Single Line-2"])
        self.assertEqual(len(list(seq.iter_effects())), 2)

    def test_backup_written(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.xsq"
            xsq.Sequence.new(5).save(p)
            xsq.Sequence.load(p).save()
            self.assertEqual(len(list(Path(td).glob("s.*.agentbak"))), 1)

    def test_times_snap_to_frames(self):
        seq = xsq.Sequence.new(5, frame_ms=25)
        fx = seq.add_effect("M", "On", 12, 1013)
        self.assertEqual((fx.get("startTime"), fx.get("endTime")), ("0", "1025"))

    def test_value_curve_format(self):
        k, v = xsq.value_curve("Bars", "Bars_Cycles", "Ramp", 10, 50)
        self.assertEqual(k, "E_VALUECURVE_Bars_Cycles")
        self.assertEqual(v, "Active=TRUE|Id=ID_VALUECURVE_Bars_Cycles|Type=Ramp|Min=0.00|Max=300.00|"
                            "P1=10.00|P2=50.00|RV=TRUE|")
        k, _ = xsq.value_curve("On", "C_SLIDER_Brightness", "Flat", 50)
        self.assertEqual(k, "C_VALUECURVE_Brightness")

    def test_color_test_builder(self):
        seq = xsq.build_color_test(["Single Line"], ["#FF0000", "#00FF00"], hold_s=1)
        self.assertEqual(seq.duration_ms, 4000)
        self.assertEqual(len(list(seq.iter_effects())), 4)

    def test_cli_smoke(self):
        for args in (["effect", "Bars"], ["layout", str(FIX)], ["info", str(FIX / "Testing.xsq")]):
            r = subprocess.run([sys.executable, str(SKILL / "scripts" / "xsq.py")] + args,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)


XL = os.environ.get("XLIGHTS_BIN") or xsq.find_xlights()
SHOW = os.environ.get("XLIGHTS_SHOW")


@unittest.skipUnless(XL and SHOW, "set XLIGHTS_SHOW (and XLIGHTS_BIN if not auto-found) for integration tests")
class TestWithXLights(unittest.TestCase):
    """Proves the documented formats against the real render engine."""

    def setUp(self):
        self.show = Path(SHOW)
        self.models = sorted(xsq.load_layout(self.show)["models"])[:1]
        self.assertTrue(self.models, "show has no models")
        self.made = []

    def tearDown(self):
        for p in self.made:
            for f in (p, p.with_suffix(".fseq")):
                if f.exists():
                    f.unlink()

    def _render(self, name, settings):
        seq = xsq.Sequence.new(10)
        for m in self.models:
            seq.add_effect(m, "Bars", 0, 10000, settings=settings, colors=["#FF0000", "#0000FF"])
        p = self.show / f"zz skilltest {name}.xsq"
        seq.save(p, backup=False)
        self.made.append(p)
        r = subprocess.run([XL, "--headless", "-s", str(self.show), str(p)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return p.with_suffix(".fseq")

    def _same(self, a, b):
        return subprocess.run([XL, "--fseqcmp", str(a), str(b)], capture_output=True).returncode == 0

    def test_value_curve_units(self):
        """Flat VC at raw 30 == static 3.0 cycles (divisor 10); raw 3 must differ."""
        base = self._render("static", {"E_TEXTCTRL_Bars_Cycles": "3.0"})
        k, v = xsq.value_curve("Bars", "Bars_Cycles", "Flat", 30)
        self.assertTrue(self._same(base, self._render("vc30", {k: v})))
        k, v = xsq.value_curve("Bars", "Bars_Cycles", "Flat", 3)
        self.assertFalse(self._same(base, self._render("vc3", {k: v})))

    def test_effects_actually_render(self):
        lit = self._render("lit", {})
        seq = xsq.Sequence.new(10)
        for m in self.models:
            seq.add_model(m)
        p = self.show / "zz skilltest empty.xsq"
        seq.save(p, backup=False)
        self.made.append(p)
        subprocess.run([XL, "--headless", "-s", str(self.show), str(p)], capture_output=True)
        self.assertFalse(self._same(lit, p.with_suffix(".fseq")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
