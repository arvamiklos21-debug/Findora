#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update keywords.txt from program.txt, applying excludes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SRC_FILE = DOCS / "program.txt"
EXCLUDE_FILE = DOCS / "exclude.txt"
OUT_FILE = DOCS / "keywords.txt"

def read_list(p: Path) -> list[str]:
    if not p.exists():
        return []
    lines = []
    with p.open("r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s or s.startswith("#"):
                continue
            s = " ".join(s.split())
            lines.append(s)
    return lines

def main() -> int:
    src = read_list(SRC_FILE)
    excl = set(x.lower() for x in read_list(EXCLUDE_FILE))
    current = read_list(OUT_FILE)

    seen_lower = set()
    dedup_src = []
    for item in src:
        key = item.lower()
        if key in seen_lower or key in excl:
            continue
        seen_lower.add(key)
        dedup_src.append(item)

    dedup_src_sorted = sorted(dedup_src, key=lambda s: s.lower())

    if dedup_src_sorted == current:
        print("No changes: keywords.txt already up-to-date.")
        return 0

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="\n") as f:
        for s in dedup_src_sorted:
            f.write(s + "\n")

    print(f"Updated {OUT_FILE} -> {len(dedup_src_sorted)} keywords "
          f"(src={len(src)}, excluded={len(excl)}).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
