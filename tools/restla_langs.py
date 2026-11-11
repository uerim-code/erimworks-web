#!/usr/bin/env python3
"""Restla tanıtım sayfasını mağaza metninden 15 dile üretir (GEO/SEO).

    python3 tools/restla_langs.py <restla-repo>/store/metadata/1.3.1-aso

Her dil için /restla/<dil>/index.html yazar: o dilin App Store adı, alt başlığı,
tanıtım metni ve açıklaması; SoftwareApplication + WebPage şeması; hreflang kümesi
(tr, en ve bu 15 dil, x-default = tr). TR ve EN sayfaların <head>'indeki hreflang
satırlarını da aynı kümeye günceller. Kaynak metin mağazayla birebir: sayfa ile
mağaza farklı şey söylemesin.

NEDEN: 2026-11-11'e kadar Restla'nın yalnız TR ve EN tanıtım sayfası vardı; diğer
dillerde Google ve yapay zekâ arama motorlarının okuyacağı bir sayfa yoktu.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
TABAN = "https://erimworks.com"
STORE = "https://apps.apple.com/app/id6787410696"
# mağaza yerelleştirmesi -> (site klasörü, hreflang / html lang)
DILLER = {
    "de": ("de", "de"), "es-ES": ("es", "es"), "fr-FR": ("fr", "fr"), "it": ("it", "it"),
    "pt-BR": ("pt", "pt"), "ru": ("ru", "ru"), "pl": ("pl", "pl"), "ja": ("ja", "ja"),
    "ko": ("ko", "ko"), "zh-Hans": ("zh", "zh-Hans"), "ar-SA": ("ar", "ar"), "hi": ("hi", "hi"),
    "id": ("id", "id"), "th": ("th", "th"), "vi": ("vi", "vi"),
}
URL_RE = re.compile(r"https?://\S+")


def alternates() -> list[tuple[str, str]]:
    out = [("tr", f"{TABAN}/restla/"), ("en", f"{TABAN}/en/restla/")]
    out += [(lang, f"{TABAN}/restla/{klasor}/") for klasor, lang in DILLER.values()]
    out.append(("x-default", f"{TABAN}/restla/"))
    return out


def alt_links() -> str:
    return "\n".join(f'<link rel="alternate" hreflang="{l}" href="{u}">' for l, u in alternates())


def blocks(desc: str) -> list[list[str]]:
    return [[ln.strip() for ln in b.split("\n") if ln.strip()] for b in re.split(r"\n\s*\n", desc.strip())]


def is_heading(line: str, block: list[str]) -> bool:
    if len(block) < 2 or len(line) > 48 or URL_RE.search(line):
        return False
    letters = [c for c in line if c.isalpha()]
    upper = letters and all(not c.islower() for c in letters)
    return bool(upper) or not re.search(r"[.。！？!?:：،؟।]$", line)


def heading_case(line: str, text: str, lang: str = "") -> str:
    """ALL-CAPS store headings -> each word's casing in mid-sentence running text.

    Sentence-initial words are skipped as evidence (they are always capitalised).
    German words not found mid-sentence are treated as nouns unless they are small
    function words.
    """
    letters = [c for c in line if c.isalpha()]
    if not letters or any(c.islower() for c in letters):
        return line
    seen: dict[str, str] = {}
    for m in re.finditer(r"[^\W\d_][\w'’-]*", text):
        w = m.group(0)
        before = text[:m.start()].rstrip(" \t\"“„«(")
        if not before or before[-1] in ".!?:\n。！？•":
            continue
        if not w.isupper() or len(w) == 1:
            seen.setdefault(w.lower(), w)
    de_small = {"und", "mit", "ohne", "für", "dein", "deine", "nur", "es", "so", "kein", "keine",
                "das", "die", "der", "im", "in", "am", "auf", "zu", "vom", "von", "oder", "offline"}
    out = []
    for i, w in enumerate(line.split(" ")):
        core = re.sub(r"^\W+|\W+$", "", w)
        low = core.lower()
        brand = {"restla": "Restla", "pro": "Pro"}
        if low in brand:
            repl = brand[low]
        elif lang != "de":
            repl = low                              # sentence case
        else:
            repl = seen.get(low)
            if repl is None or (repl.islower() and low not in de_small and i > 0 and not seen.get(low, "").islower()):
                repl = core[:1] + low[1:] if low not in de_small else low
            repl = "-".join(x[:1].upper() + x[1:] if k else x for k, x in enumerate(repl.split("-")))
        if i == 0:
            repl = repl[:1].upper() + repl[1:]
        out.append(w.replace(core, repl) if core else w)
    return " ".join(out)

def linkify(text: str) -> str:
    esc = html.escape(text)
    return URL_RE.sub(lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>', esc)


def page(meta: dict, klasor: str, lang: str, head_tail: str, header: str, footer: str) -> str:
    url = f"{TABAN}/restla/{klasor}/"
    title = f"{meta['name']} – {meta['subtitle']}"
    desc_meta = meta["promotionalText"]
    bl = blocks(meta["description"])
    intro, rest = bl[0], bl[1:]
    body = []
    for b in rest:
        if all(URL_RE.search(x) for x in b):          # legal links block
            body.append('<p class="links">' + "<br>".join(linkify(x) for x in b) + "</p>")
            continue
        if is_heading(b[0], b):
            body.append(f'<section class="read"><div class="section-head"><h2>{html.escape(heading_case(b[0], meta["description"], lang))}</h2></div>')
            body += [f"<p>{linkify(x)}</p>" for x in b[1:]]
            body.append("</section>")
        else:
            body.append('<section class="read">' + "".join(f"<p>{linkify(x)}</p>" for x in b) + "</section>")
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": ["SoftwareApplication", "MobileApplication"], "@id": f"{TABAN}/restla/#app",
             "name": "Restla", "alternateName": meta["name"], "applicationCategory": "ProductivityApplication",
             "operatingSystem": "iOS", "url": url, "installUrl": STORE, "downloadUrl": STORE,
             "image": f"{TABAN}/assets/apps/restla.png", "description": desc_meta, "inLanguage": lang,
             "offers": [{"@type": "Offer", "price": "0", "priceCurrency": "USD", "url": STORE}],
             "publisher": {"@type": "Organization", "@id": f"{TABAN}/#org", "name": "Erimworks", "url": f"{TABAN}/"}},
            {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "inLanguage": lang,
             "isPartOf": {"@id": f"{TABAN}/#site"}, "about": {"@id": f"{TABAN}/restla/#app"},
             "publisher": {"@id": f"{TABAN}/#org"}},
        ],
    }
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    return f"""<!doctype html>
<html lang="{lang}"{dir_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{url}">
{alt_links()}
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc_meta)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Erimworks">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc_meta)}">
<meta property="og:image" content="{TABAN}/assets/og-erimworks.png">
<meta name="twitter:card" content="summary_large_image">
{head_tail}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
{header}
<main id="content" class="wrap">
  <p class="crumbs"><a href="/en/">Erimworks</a><span>/</span><a href="/en/restla/">Restla</a><span>/</span>{html.escape(lang)}</p>
  <div class="read">
    <div class="top">
      <img src="/apps/restla.png?v=1.3.0" alt="Restla" width="64" height="64">
      <h1>{html.escape(meta['name'])}</h1>
    </div>
    <p class="lede">{"<br>".join(linkify(x) for x in intro)}</p>
    <div class="actions">
      <a class="btn btn-primary" href="{STORE}" rel="noopener">App Store</a>
      <a class="btn btn-quiet" href="/en/restla/" hreflang="en" lang="en">English</a>
    </div>
  </div>
  {chr(10).join(body)}
</main>
{footer}
</body>
</html>
"""


def main() -> int:
    src = pathlib.Path(sys.argv[1])
    en = (KOK / "en/restla/index.html").read_text(encoding="utf-8")
    css = re.search(r'<meta name="theme-color".*?(?=<style>|<script type="application/ld)', en, re.S).group(0).strip()
    consent = re.search(r'<script src="/assets/cerez\.js[^"]*" defer></script>', en).group(0)
    head_tail = css + "\n" + consent
    header = en[en.index("<body>") + 6: en.index("<main")].strip()
    header = re.sub(r'<nav class="lang".*?</nav>', "", header, flags=re.S)
    footer = en[en.index("<footer"): en.index("</footer>") + 9]
    for loc, (klasor, lang) in DILLER.items():
        meta = json.loads((src / f"{loc}.json").read_text(encoding="utf-8"))
        out = KOK / "restla" / klasor / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(meta, klasor, lang, head_tail, header, footer), encoding="utf-8")
        print("yazıldı", out.relative_to(KOK))
    # TR ve EN sayfaların kümesini de genişlet
    for f in ("restla/index.html", "en/restla/index.html"):
        p = KOK / f
        s = p.read_text(encoding="utf-8")
        s = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+', alt_links() + "\n", s, count=1)
        p.write_text(s, encoding="utf-8")
        print("güncellendi", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
