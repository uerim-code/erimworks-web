#!/usr/bin/env python3
"""TR ↔ EN sayfa çiftlerini denetler (yayın öncesi kapı; her zaman --check).

    python3 tools/hreflang.py        # sorun varsa 1 ile çıkar

Her sayfada hreflang taşıyan <link rel="alternate"> varsa:
- küme tam olarak {tr, en, x-default} olmalı, x-default = tr
- sayfanın kendi dili kendi canonical'ını göstermeli
- karşı sayfa var olmalı, aynı alternatif kümesini taşımalı, <html lang> uymalı
- JSON-LD geçerli olmalı; WebPage.url canonical'a, inLanguage <html lang>'a eşit
- FAQPage soru/cevapları görünür <details> içeriğiyle birebir aynı olmalı
- EN sayfadaki ürün @id'si /en/ altında OLMAMALI (TR köküyle aynı varlık)
- sayfadaki /en/... bağlantıları var olan dosyalara gitmeli

NEDEN: İngilizce sayfalar 2026-11-04'te ayrı /en/ adresleri olarak açıldı.
Bir çiftin tek tarafı güncellenirse Google hreflang kümesini sessizce yok sayar
ve EN sayfa TR'nin kopyası gibi değerlendirilir; hata konsolda görünmez.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
TABAN = "https://erimworks.com"


def main() -> int:
    sayfalar: dict[str, dict] = {}
    for f in sorted(KOK.rglob("*.html")):
        if "node_modules" in f.parts:
            continue
        s = f.read_text(encoding="utf-8")
        bas = s[: s.find("</head>")]
        alts = {m.group(1): m.group(2) for m in re.finditer(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', bas)}
        if not alts:
            continue
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', bas)
        dil = re.search(r'<html lang="([^"]+)"', s)
        sayfalar[canon.group(1) if canon else str(f)] = {"f": f, "lang": dil.group(1) if dil else "?", "alts": alts, "s": s}

    hatalar: list[str] = []
    for u, p in sayfalar.items():
        a = p["alts"]
        if set(a) != {"tr", "en", "x-default"}:
            hatalar.append(f"{u}: hreflang kümesi {sorted(a)}")
            continue
        if a[p["lang"]] != u:
            hatalar.append(f"{u}: kendi dili ({p['lang']}) {a[p['lang']]} gösteriyor")
        if a["x-default"] != a["tr"]:
            hatalar.append(f"{u}: x-default ≠ tr")
        for dil in ("tr", "en"):
            diger = sayfalar.get(a[dil])
            if not diger:
                hatalar.append(f"{u}: {dil} hedefi yok: {a[dil]}")
            elif diger["alts"] != a:
                hatalar.append(f"{u}: alternatifler {a[dil]} ile uyuşmuyor")
            elif diger["lang"] != dil:
                hatalar.append(f"{u}: {a[dil]} sayfasında lang={diger['lang']}")
        for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p["s"], re.S):
            try:
                d = json.loads(blok)
            except ValueError as e:
                hatalar.append(f"{u}: JSON-LD geçersiz: {e}")
                continue
            g = d.get("@graph", [d])
            wp = [n for n in g if n.get("@type") == "WebPage"]
            if not wp or wp[0].get("url") != u or wp[0].get("inLanguage") != p["lang"]:
                hatalar.append(f"{u}: WebPage url/inLanguage canonical ve <html lang> ile uyuşmuyor")
            for n in g:
                if n.get("@type") == "FAQPage":
                    sema = [(q["name"], q["acceptedAnswer"]["text"]) for q in n["mainEntity"]]
                    gorunur = [(html.unescape(m.group(1)).strip(), html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip())
                               for m in re.finditer(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", p["s"], re.S)]
                    if sema != gorunur:
                        hatalar.append(f"{u}: FAQPage şeması görünür SSS ile birebir değil")
                if "/en/" in u and isinstance(n.get("@type"), list) and "SoftwareApplication" in n["@type"] and "/en/" in n.get("@id", ""):
                    hatalar.append(f"{u}: ürün @id'si /en/ altında; TR köküyle aynı olmalı")
        for href in set(re.findall(r'href="(/en/[^"#]*)"', p["s"])):
            if not (KOK / href.lstrip("/") / "index.html").exists():
                hatalar.append(f"{u}: kırık bağlantı {href}")

    if hatalar:
        print("\n".join(hatalar))
        return 1
    print(f"hreflang güncel ({len(sayfalar)} sayfa, {len(sayfalar) // 2} çift).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
