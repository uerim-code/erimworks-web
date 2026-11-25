#!/usr/bin/env python3
"""Uygulama hukuki sayfalarını (privacy.html, terms.html) siteye link vermeyen
"çıkmaz" sayfalara çevirir.

    python3 tools/hukuki_cikmaz.py            # dönüştür
    python3 tools/hukuki_cikmaz.py --check    # siteye link kalmışsa 1 ile çık

NEDEN: Bu sayfaları mobil uygulamalar açıyor (paywall ve ayarlardaki Gizlilik /
Koşullar linkleri). Sayfanın kendisinde çerez bandı yok (`tools/cerez.py` bunu
denetliyor), ama üst menü ve altbilgi `/`, `/gizlilik/`, `/hakkimizda/`,
`/iletisim/` gibi bandlı sayfalara gidiyordu. Apple incelemecisi bir tıkla bandı
görüp bunu "ATT'de 'takip etme' diyen kullanıcıya çerez soruluyor" diye okudu:
Restla 1.3.4, 25 Kas 2026'da Guideline 5.1.1(iv) ile reddedildi (1.3.1'den sonra
ikinci kez). Uygulamanın açtığı web içeriğinden bandlı hiçbir sayfaya
ulaşılamamalı.

Kalan linkler: sayfa içi çapalar, aynı klasördeki hukuki sayfalar (privacy <->
terms), site varlıkları (css, ikon), mailto ve harici adresler (Apple EULA,
Google gizlilik politikası gibi).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ADLAR = ("privacy.html", "terms.html")
VARLIK = re.compile(r'^/(assets/|favicon|apple-touch-icon)')
# Başka bir hukuki sayfa da bandsızdır (ör. /restla/tr/privacy -> /restla/privacy).
HUKUKI = re.compile(r'/(privacy|terms)(\.html)?/?(#.*)?$')


def sayfalar() -> list[Path]:
    return sorted(p for p in KOK.rglob("*.html")
                  if p.name in ADLAR and "node_modules" not in p.parts and ".git" not in p.parts)


SITE = re.compile(r'https?://(www\.)?erimworks\.com(?=[/"#?]|$)')


def goreli(href: str) -> str:
    """https://erimworks.com/x -> /x ; https://erimworks.com -> /"""
    return SITE.sub('', href) or '/' if SITE.match(href) else href


def donustur(html: str) -> str:
    # Üst menü: kelime işareti link olmaktan çıkar, menü kalkar.
    html = re.sub(r'<a class="wordmark" href="[^"]*">([^<]*)</a>', r'<span class="wordmark">\1</span>', html)
    html = re.sub(r'\s*<nav class="site-nav"[^>]*>.*?</nav>', "", html, flags=re.S)
    # Altbilgi: site içi linkler (ve aralarındaki ayraçlar) kalkar; telif ve e-posta kalır.
    def altbilgi(m: re.Match) -> str:
        blok = m.group(0)
        blok = re.sub(r'\s*<a href="/[^"]*">[^<]*</a>(\s*·)?', "", blok)
        blok = re.sub(r'(</span>)\s*·\s*', r"\1 ", blok)
        return blok
    html = re.sub(r'<footer class="site-foot">.*?</footer>', altbilgi, html, flags=re.S)
    # Gövdede kalan site içi linkler (varlık ve aynı klasör hariç) düz metne döner.
    def govde(m: re.Match) -> str:
        href, metin = m.group(1), m.group(2)
        if href.startswith("/") and not VARLIK.match(href) and not HUKUKI.search(href):
            return metin
        return m.group(0)
    html = re.sub(r'<a href="(/[^"]*)">(.*?)</a>', govde, html, flags=re.S)
    # Tam adresli site linkleri (https://erimworks.com/...) de aynı kurala tabi.
    def tam(m: re.Match) -> str:
        href, metin = goreli(m.group(1)), m.group(2)
        if not VARLIK.match(href) and not HUKUKI.search(href):
            return metin
        return m.group(0)
    html = re.sub(r'<a href="(https?://(?:www\.)?erimworks\.com[^"]*)"[^>]*>(.*?)</a>', tam, html, flags=re.S)
    return html


def site_linkleri(html: str) -> list[str]:
    out = []
    for h in re.findall(r'<a [^>]*href="([^"]+)"', html):
        g = goreli(h)
        if g.startswith("/") and not VARLIK.match(g) and not HUKUKI.search(g):
            out.append(h)
    return out


def main() -> int:
    check = "--check" in sys.argv
    hatali = []
    for p in sayfalar():
        eski = p.read_text(encoding="utf-8")
        yeni = donustur(eski)
        if check:
            kalan = site_linkleri(eski)
            if kalan:
                hatali.append(f"{p.relative_to(KOK)}: {', '.join(sorted(set(kalan)))}")
            continue
        if yeni != eski:
            p.write_text(yeni, encoding="utf-8")
        kalan = site_linkleri(yeni)
        if kalan:
            hatali.append(f"{p.relative_to(KOK)}: {', '.join(sorted(set(kalan)))}")
    print(f"{len(sayfalar())} hukuki sayfa denetlendi")
    for h in hatali:
        print("  SİTEYE LİNK:", h)
    return 1 if hatali else 0


if __name__ == "__main__":
    sys.exit(main())
