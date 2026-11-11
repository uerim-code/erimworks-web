#!/usr/bin/env python3
"""Çerez rızası betiğini her yayın sayfasının <head>'ine koyar ve damgalar.

    python3 tools/cerez.py            # etiketi ekle / damgayı tazele
    python3 tools/cerez.py --check    # eksik ya da bayatsa 1 ile çık

NEDEN ARAÇ — İKİ AYRI UNUTMA:

1. **Eksik sayfa.** Rıza bandı 88 sayfanın 87'sinde olursa, kalan sayfa
   ziyaretçiye hiçbir şey sormadan ölçülür. Bir sayfa eklendiğinde etiketi
   elle koymayı unutmak, kuralı tamamen uygulamamaktan daha kötüdür: eksik
   olduğu görünmez.

2. **Bayat damga.** `assets.py`'nin `site.css` için çözdüğü sorunun aynısı
   `cerez.js` için de geçerli — `_headers` `/assets/*` için yedi günlük
   önbellek veriyor ve Cloudflare adrese göre önbelleğe alıyor. Damga
   olmadan, rıza mantığındaki bir düzeltme ziyaretçiye bir hafta ulaşmaz.
   Bu dosyada düzeltilecek şey insanların izlenme tercihi olduğu için
   gecikme kabul edilebilir değil.

Etiket `</head>`in hemen öncesine, `defer` ile girer: betik sayfayı
bloklamaz ama DOM hazır olduğunda bant kurulur.
"""
from __future__ import annotations

import hashlib
import re
import sys

from sayfalar import KOK, sayfalar

BETIK = KOK / "assets" / "cerez.js"

# <script ... src="/assets/cerez.js[?v=...]" ...></script>
DESEN = re.compile(r'[ \t]*<script[^>]*src="/assets/cerez\.js(?:\?v=[0-9a-f]+)?"[^>]*></script>\n?')


def damga() -> str:
    return hashlib.sha256(BETIK.read_bytes()).hexdigest()[:10]


def etiket() -> str:
    return f'<script src="/assets/cerez.js?v={damga()}" defer></script>\n'


def yaz(kontrol: bool) -> int:
    hedef = etiket()
    bayat: list[str] = []
    yazildi = 0

    for yol in sayfalar():
        metin = yol.read_text(encoding="utf-8")
        mevcut = DESEN.search(metin)

        if mevcut and mevcut.group(0).strip() == hedef.strip():
            continue

        if kontrol:
            bayat.append(f"{yol.relative_to(KOK)}: {'damga bayat' if mevcut else 'çerez betiği YOK'}")
            continue

        if mevcut:
            yeni = DESEN.sub(hedef, metin, count=1)
        else:
            if "</head>" not in metin:
                bayat.append(f"{yol.relative_to(KOK)}: </head> yok, elle bakılmalı")
                continue
            yeni = metin.replace("</head>", hedef + "</head>", 1)

        yol.write_text(yeni, encoding="utf-8")
        yazildi += 1

    if kontrol:
        if bayat:
            print("\n".join(bayat))
            print("Düzeltmek için: python3 tools/cerez.py")
            return 1
        print(f"çerez betiği güncel (?v={damga()}, {len(sayfalar())} sayfa).")
        return 0

    if bayat:
        print("\n".join(bayat))
        return 1
    print(f"çerez betiği yazıldı: ?v={damga()} — {yazildi} sayfa güncellendi.")
    return 0


if __name__ == "__main__":
    sys.exit(yaz("--check" in sys.argv))
