#!/usr/bin/env python3
"""Monthly check: has the Revenue Department changed any official form we ship?

    python3 tools/check_forms.py            # report only
    python3 tools/check_forms.py --record   # store current hashes in catalog.json (after an approved update)

For every form in assets/forms/catalog.json, downloads its `source` URL from rd.go.th / sso.go.th,
compares the SHA-256 with the hash recorded in the catalog and with the bundled PDF, and checks
that every mapped box still exists in the new file. Prints a JSON report; exit code 1 when
anything changed or could not be checked.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "plugins" / "thaitax-assistant" / "assets" / "forms"
CATALOG = FORMS / "catalog.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fetch(url: str, dest: Path, tries: int = 6) -> None:
    """rd.go.th often resets connections or answers with an HTML page: retry with a pause."""
    last = "unknown error"
    for i in range(tries):
        try:
            subprocess.run(["curl", "-sSL", "-m", "120", "-A", "Mozilla/5.0 ThaiTaxAssistant-monthly-check", "-o", str(dest), url],
                           check=True, capture_output=True)
            if dest.read_bytes().startswith(b"%PDF"):
                return
            last = "download is not a PDF"
        except subprocess.CalledProcessError as e:
            last = (e.stderr or b"").decode(errors="ignore").strip() or f"curl exit {e.returncode}"
        time.sleep(5 * (i + 1))
    raise RuntimeError(last)


def field_names(pdf: Path) -> set[str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return set()
    return set((PdfReader(str(pdf)).get_fields() or {}).keys())


def mapped_fields(map_file: Path) -> set[str]:
    m = json.loads(map_file.read_text(encoding="utf-8")).get("fields", {})
    out = set()
    for v in m.values():
        name = v if isinstance(v, str) else (v or {}).get("field")
        if name:
            out.add(name.split("#")[0])
    return out


def main(record: bool) -> int:
    cat = json.loads(CATALOG.read_text(encoding="utf-8"))
    report = {"unchanged": [], "changed": [], "errors": []}
    tmp = Path(tempfile.mkdtemp())
    for key, info in cat.items():
        url = info.get("source")
        local = FORMS / info["file"]
        if not url:
            report["errors"].append({"form": key, "error": "no source URL"})
            continue
        dl = tmp / info["file"]
        time.sleep(3)  # be gentle with rd.go.th
        try:
            fetch(url, dl)
        except Exception as e:  # network, 404, not a PDF
            report["errors"].append({"form": key, "url": url, "error": str(e)})
            continue
        new_hash = sha(dl)
        recorded = info.get("sha256") or sha(local)
        if record:
            info["sha256"] = new_hash
        if new_hash == recorded:
            report["unchanged"].append(key)
            continue
        entry = {"form": key, "url": url, "old_sha256": recorded, "new_sha256": new_hash, "downloaded_to": str(dl)}
        if info.get("map"):
            missing = sorted(mapped_fields(FORMS / info["map"]) - field_names(dl))
            entry["mapped_boxes_missing_in_new_file"] = missing
            entry["map_still_fits"] = not missing
        report["changed"].append(entry)
    if record:
        CATALOG.write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    report["summary"] = f'{len(report["unchanged"])} unchanged, {len(report["changed"])} changed, {len(report["errors"])} could not be checked'
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if report["changed"] or report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main("--record" in sys.argv))
