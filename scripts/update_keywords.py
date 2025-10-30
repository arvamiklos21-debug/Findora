from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

KW_FILE = DOCS / "keywords.txt"
PROGRAM_FILE = DOCS / "program.txt"
EXCLUDE_FILE = DOCS / "exclude.txt"

def read_lines(p: Path) -> list[str]:
    if not p.exists():
        return []
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines()]

def normalize(items: list[str]) -> list[str]:
    out = []
    for s in items:
        if not s:
            continue
        s = " ".join(s.split())
        out.append(s)
    return out

def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    base = normalize(read_lines(KW_FILE))
    extra = normalize(read_lines(PROGRAM_FILE))
    exclude = set(x.lower() for x in normalize(read_lines(EXCLUDE_FILE)))
    combined = base + extra

    seen_lower = set()
    unique = []
    for item in combined:
        key = item.lower()
        if key in exclude:
            continue
        if key not in seen_lower:
            seen_lower.add(key)
            unique.append(item)

    unique.sort(key=lambda s: s.casefold())

    old_text = KW_FILE.read_text(encoding="utf-8") if KW_FILE.exists() else ""
    new_text = "\n".join(unique).rstrip() + ("\n" if unique else "")
    if new_text != old_text:
        KW_FILE.write_text(new_text, encoding="utf-8")
        print(f"Updated {KW_FILE} with {len(unique)} keywords.")
    else:
        print("No changes to keywords.txt")

if __name__ == "__main__":
    main()
