import os
from pathlib import Path
import datetime

# --- Alapbeállítások ---
ROOT = Path(__file__).parent
DOCS = ROOT / "docs"        # ide generáljuk az oldalt
TEMPLATE = ROOT / "template.html"
KEYWORDS_FILE = ROOT / "keywords.txt"

# A te weboldalad alap URL-je (!!! fontos !!!)
SITE_BASE = "https://arvamiklos21-debug.github.io/akcios-bot"

# --- Fájlok betöltése ---
def load_template():
    return TEMPLATE.read_text(encoding="utf-8")

def load_keywords():
    return [k.strip() for k in KEYWORDS_FILE.read_text(encoding="utf-8").splitlines() if k.strip()]

# --- HTML generálás ---
def generate_page(template, keyword):
    html = template.replace("{{keyword}}", keyword)
    html = html.replace("{{title}}", f"Akciós {keyword} árak és ajánlatok")
    html = html.replace("{{date}}", datetime.datetime.now().strftime("%Y.%m.%d."))
    return html

# --- Fő folyamat ---
def main():
    DOCS.mkdir(exist_ok=True)

    template = load_template()
    keywords = load_keywords()

    index_links = []

    for kw in keywords:
        filename = kw.replace(" ", "_").lower() + ".html"
        filepath = DOCS / filename
        html = generate_page(template, kw)
        filepath.write_text(html, encoding="utf-8")
        index_links.append(f'<li><a href="{filename}">{kw}</a></li>')

    index_html = f"""
    <html>
    <head><meta charset='utf-8'><title>Akciós kereső</title></head>
    <body>
        <h1>Akciós termékek kulcsszavak szerint</h1>
        <ul>
            {''.join(index_links)}
        </ul>
        <p>Készült: {datetime.datetime.now().strftime('%Y.%m.%d.')}</p>
    </body>
    </html>
    """

    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print(f"✅ {len(keywords)} oldal generálva a /docs mappába.")

if __name__ == "__main__":
    main()
