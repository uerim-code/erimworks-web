#!/usr/bin/env python3
"""sitemap.xml'i depodaki HTML dosyalarından üretir.

    python3 tools/sitemap.py            # sitemap.xml'i yaz
    python3 tools/sitemap.py --check    # bayatsa 1 ile çık (yayın öncesi kapı)

KURALLAR
- Bir sayfa sitemap'e girer ⇔ canonical'ı kendi adresini gösteriyor VE
  noindex değil VE hukuki/destek sayfası değil (privacy, terms, support,
  delete-account). Hukuki sayfalar indekslenebilir kalır; sitemap yalnız
  ticari ve kurumsal sayfaları öne çıkarır (36 → ~19 URL, 2026-11-03).
- <lastmod>: dosyanın son commit tarihi (git log -1). Çalışma ağacında
  değişmiş ya da henüz commit edilmemiş dosya için bugünün tarihi.
- <priority> yazılmaz: Google yok sayar, Bing dikkate almaz.
- Adres biçimi: index.html → "/dizin/", diğer → "/dizin/ad" (uzantısız;
  Cloudflare Pages .html'i 308 ile uzantısıza çevirir).
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import subprocess
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
TABAN = "https://erimworks.com"
HUKUKI = {"privacy", "terms", "support", "delete-account"}


def adres(f: pathlib.Path) -> str:
    rel = f.relative_to(KOK)
    if rel.name == "index.html":
        yol = "/" + "/".join(rel.parts[:-1])
        return TABAN + (yol if yol.endswith("/") else yol + "/")
    return TABAN + "/" + "/".join(rel.parts[:-1] + (rel.stem,))


def son_degisim(f: pathlib.Path) -> str:
    rel = str(f.relative_to(KOK))
    durum = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=KOK, capture_output=True, text=True).stdout.strip()
    if durum:  # değişmiş ya da takipsiz
        return dt.date.today().isoformat()
    tarih = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=KOK, capture_output=True, text=True).stdout.strip()
    return tarih or dt.date.today().isoformat()


def sayfalar() -> list[tuple[str, str]]:
    cikti: list[tuple[str, str]] = []
    for f in sorted(KOK.rglob("*.html")):
        if "node_modules" in f.parts or f.name == "404.html":
            continue
        if f.stem in HUKUKI:
            continue
        metin = f.read_text(encoding="utf-8", errors="replace")
        bas = metin[: metin.find("</head>")] if "</head>" in metin else metin
        if re.search(r'<meta name="robots" content="[^"]*noindex', bas):
            continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', bas)
        u = adres(f)
        if not m or m.group(1) != u:
            continue
        cikti.append((u, son_degisim(f)))
    # kök en üstte, sonra adrese göre
    cikti.sort(key=lambda x: (x[0] != TABAN + "/", x[0]))
    return cikti


def xml() -> str:
    satirlar = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, tarih in sayfalar():
        satirlar += ["  <url>", f"    <loc>{u}</loc>", f"    <lastmod>{tarih}</lastmod>", "  </url>"]
    satirlar.append("</urlset>")
    return "\n".join(satirlar) + "\n"


def main() -> int:
    yol = KOK / "sitemap.xml"
    yeni = xml()
    if "--check" in sys.argv:
        eski = yol.read_text(encoding="utf-8") if yol.exists() else ""
        # lastmod farkı tek başına bayatlık sayılmaz; adres kümesi karşılaştırılır
        locs = lambda s: re.findall(r"<loc>([^<]+)</loc>", s)
        if locs(eski) != locs(yeni):
            print("sitemap.xml BAYAT: adres kümesi sayfalarla uyuşmuyor. Düzeltmek için: python3 tools/sitemap.py")
            return 1
        print(f"sitemap.xml güncel ({len(locs(yeni))} adres).")
        return 0
    yol.write_text(yeni, encoding="utf-8")
    print(f"sitemap.xml yazıldı — {yeni.count('<loc>')} adres.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
