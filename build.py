# build.py
from datetime import date
from pathlib import Path
from slugify import slugify
from jinja2 import Template
import urllib.parse

# ==== ÁLLÍTHATÓ (később cseréld a sajátodra) ====
SITE_BASE = "https://felhasznalonev.github.io"   # GitHub Pages URL-ed
AMAZON_TAG = "TE-ASSOCIATE-ID-21"                # Amazon affiliate tag (ha van)
# ================================================

ROOT = Path(__file__).parent
PAGES = ROOT / "pages"
PAGES.mkdir(exist_ok=True)

# sablon és kulcsszavak beolvasása
template = Template((ROOT / "template.html").read_text(encoding="utf-8"))
kw_file = ROOT / "keywords.txt"
if not kw_file.exists():
    raise SystemExit("Hiányzik a keywords.txt a projekt gyökerében.")
keywords = [l.strip() for l in kw_file.read_text(encoding="utf-8").splitlines() if l.strip()]

def amazon_search_url(query: str) -> str:
    """Amazon kereső link affiliate taggel (teszteléshez tökéletes)."""
    base = "https://www.amazon.com/s"
    url = base + "?" + urllib.parse.urlencode({"k": query})
    if AMAZON_TAG:
        url += f"&tag={AMAZON_TAG}"
    return url

def fake_products_for(keyword: str):
    """8 dummy ‘termék’ – később igazi forrásra cseréljük."""
    return [
        {"title": f"{keyword.title()} #{i+1}", "price": None, "url": amazon_search_url(keyword)}
        for i in range(8)
    ]

def build_one(keyword: str):
    slug = slugify(keyword)
    title = f"Akciós {keyword} – {date.today().strftime('%Y. %B')}"
    html = template.render(
        title=title,
        description=f"{keyword} friss akciók – naponta frissítve.",
        canonical=f"{SITE_BASE}/{slug}.html",
        heading=title,
        updated=date.today().isoformat(),
        products=fake_products_for(keyword),
    )
    (PAGES / f"{slug}.html").write_text(html, encoding="utf-8")
    return slug, title

def build_index(slugs_titles):
    links = "\n".join([f'<li><a href="{slug}.html">{title}</a></li>' for slug, title in slugs_titles])
    html = f"""<!doctype html><html lang="hu"><head>
<meta charset="utf-8"><title>Akciós oldalak – index</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head><body><h1>Akciós gyűjtő – kulcsszó oldalak</h1>
<ol>{links}</ol>
<p>Frissítve: {date.today().isoformat()}</p>
</body></html>"""
    (PAGES / "index.html").write_text(html, encoding="utf-8")

def build_sitemap(slugs):
    urls = [f"{SITE_BASE}/{s}.html" for s, _ in slugs] + [f"{SITE_BASE}/index.html"]
    body = "\n".join([f"<url><loc>{u}</loc></url>" for u in urls])
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'
    (PAGES / "sitemap.xml").write_text(xml, encoding="utf-8")

def main():
    slugs_titles = [build_one(kw) for kw in keywords]
    build_index(slugs_titles)
    build_sitemap(slugs_titles)
    print(f"OK – {len(slugs_titles)} oldal generálva a /pages mappába.")

if __name__ == "__main__":
    main()
