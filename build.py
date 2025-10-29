from pathlib import Path
import datetime
import urllib.parse

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "template.html"
KEYWORDS = ROOT / "keywords.txt"

# 🔑 Amazon affiliate tag-ed:
AMAZON_TAG = "akciosbot21-20"

# GitHub Pages alap URL (SEO-hoz használjuk, maradhat így)
SITE_BASE = "https://arvamiklos21-debug.github.io/akcios-bot"

def load_template() -> str:
    return TEMPLATE.read_text(encoding="utf-8")

def load_keywords() -> list[str]:
    return [k.strip() for k in KEYWORDS.read_text(encoding="utf-8").splitlines() if k.strip()]

def amazon_search_url(keyword: str) -> str:
    # https://www.amazon.com/s?k=<kulcsszó>&tag=<tag>
    q = {"k": keyword}
    base = "https://www.amazon.com/s?" + urllib.parse.urlencode(q)
    return f"{base}&tag={AMAZON_TAG}" if AMAZON_TAG else base

def render_page(tpl: str, kw: str) -> str:
    # A template az {{amazon_url}} helyére kapja a tagelt keresőlinket
    return (tpl
            .replace("{{title}}", f"Akciós {kw} – ajánlatok")
            .replace("{{keyword}}", kw)
            .replace("{{date}}", datetime.datetime.now().strftime("%Y.%m.%d."))
            .replace("{{amazon_url}}", amazon_search_url(kw))
           )

def main():
    DOCS.mkdir(exist_ok=True)
    tpl = load_template()
    keywords = load_keywords()

    links = []
    for kw in keywords:
        filename = kw.replace(" ", "_").lower() + ".html"
        (DOCS / filename).write_text(render_page(tpl, kw), encoding="utf-8")
        links.append(f'<li><a href="{filename}">{kw}</a></li>')

    index = f"""<!doctype html><html lang="hu"><meta charset="utf-8">
<title>Akciós kulcsszavak</title>
<body>
<h1>Akciós kulcsszavak</h1>
<ol>{''.join(links)}</ol>
<p>Frissítve: {datetime.datetime.now().strftime('%Y.%m.%d.')}</p>
</body></html>"""
    (DOCS / "index.html").write_text(index, encoding="utf-8")
    print(f"✅ {len(keywords)} oldal generálva a /docs mappába. Tag: {AMAZON_TAG}")

if __name__ == "__main__":
    main()
