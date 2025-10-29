from pathlib import Path
import datetime

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"            # IDE fog generálni
TEMPLATE = ROOT / "template.html"
KEYWORDS = ROOT / "keywords.txt"

SITE_BASE = "https://arvamiklos21-debug.github.io/akcios-bot"  # GitHub Pages URL-ed

def load_template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")

def load_keywords() -> list[str]:
    return [k.strip() for k in KEYWORDS.read_text(encoding="utf-8").splitlines() if k.strip()]

def page_html(tpl: str, kw: str) -> str:
    # Egyszerű helyettesítés – a template.html-nek ezeket a jelölőket kell tartalmaznia
    return (tpl
            .replace("{{title}}", f"Akciós {kw} – ajánlatok")
            .replace("{{keyword}}", kw)
            .replace("{{date}}", datetime.datetime.now().strftime("%Y.%m.%d."))
           )

def main():
    DOCS.mkdir(exist_ok=True)

    tpl = load_template()
    keywords = load_keywords()

    links = []
    for kw in keywords:
        name = kw.replace(" ", "_").lower() + ".html"
        (DOCS / name).write_text(page_html(tpl, kw), encoding="utf-8")
        links.append(f'<li><a href="{name}">{kw}</a></li>')

    index = f"""<!doctype html><html lang="hu"><meta charset="utf-8">
<title>Akciós kulcsszavak</title>
<body>
<h1>Akciós kulcsszavak</h1>
<ol>{''.join(links)}</ol>
<p>Frissítve: {datetime.datetime.now().strftime('%Y.%m.%d.')}</p>
</body></html>"""
    (DOCS / "index.html").write_text(index, encoding="utf-8")
    print(f"✅ {len(keywords)} oldal generálva a /docs mappába. URL: {SITE_BASE}/")

if __name__ == "__main__":
    main()
