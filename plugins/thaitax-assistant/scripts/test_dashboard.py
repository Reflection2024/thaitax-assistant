#!/usr/bin/env python3
"""Tests for dashboard.py: every example spec renders, Hebrew renders right to left, bad specs fail loudly."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dashboard  # noqa: E402

EX = sorted(glob.glob(os.path.join(HERE, "..", "assets", "dashboards", "*.json")))


def test_examples_render():
    assert len(EX) == 6, EX
    for p in EX:
        spec = json.load(open(p, encoding="utf-8"))
        out = dashboard.render(spec)
        assert out.startswith("<!DOCTYPE html>"), p
        assert out.count('class="card"') == len(spec["sections"]), p
        assert 'dir="ltr"' in out
        for k in spec["kpis"]:
            assert dashboard.e(k["value"]) in out, (p, k)


def test_hebrew_rtl_and_isolated_numbers():
    spec = json.load(open(os.path.join(HERE, "..", "assets", "dashboards", "monthly-tax.json"), encoding="utf-8"))
    spec["lang"] = "he"
    spec["title"] = "המסים של החודש"
    out = dashboard.render(spec)
    assert 'dir="rtl"' in out and 'lang="he"' in out
    assert "<bdi>฿10,605</bdi>" in out


def test_any_language_and_escaping():
    out = dashboard.render({"lang": "ru", "title": "Налоги <b>", "kpis": [], "sections": [{"type": "list", "title": "x", "items": [{"text": "a&b"}]}]})
    assert 'dir="ltr"' in out and "Налоги &lt;b&gt;" in out and "a&amp;b" in out


def test_unknown_section_fails():
    try:
        dashboard.render({"sections": [{"type": "pie"}]})
    except ValueError:
        return
    raise AssertionError("unknown section type should fail")


if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); n += 1
    print(f"ok {n} tests")
