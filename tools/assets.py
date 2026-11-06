#!/usr/bin/env python3
"""Stil dosyasının adresine içerik damgası basar (cache-busting).

    python3 tools/assets.py            # HTML'lerdeki ?v= damgasını güncelle
    python3 tools/assets.py --check    # bayatsa 1 ile çık (yayın öncesi kapı)

NEDEN VAR — ÖLÇÜLDÜ, TAHMİN DEĞİL: 2026-11-06'da canlı sitede HTML yeniydi
ama `/assets/site.css` BEŞ GÜNLÜK bir kopyaydı (`age: 435322`,
`cf-cache-status: HIT`). Sebep ikisinin birleşimi:

  _headers → /assets/*  : max-age=604800 (yedi gün)
  dosya adı             : hiç değişmiyor

Cloudflare adrese göre önbelleğe alır. Dosya adı sabit kalınca kenar
sunucudaki eski nesne yedi gün boyunca yerinde durur; Pages'e yapılan
dağıtım onu DÜŞÜRMEZ. Sonuç en kötü hâli: taze HTML + bayat CSS. Yani
sayfa, henüz var olmayan sınıflara atıfta bulunan işaretlemeyle açılır.

ÇÖZÜM — kenar sunucuya dokunmadan: adresin sonuna CSS'in kendi sha256'sından
türeyen bir damga eklenir. CSS değişince damga değişir, damga değişince adres
değişir, yeni adres kenar sunucuda HİÇ görülmediği için ıskalanır ve taze
çekilir. HTML'in kendi önbelleği kısa (max-age=600) olduğu için yeni adres
ziyaretçiye on dakika içinde ulaşır.

Bu yüzden /assets/* için UZUN önbellek artık doğru: damga olmadan tehlike,
damgayla avantaj.
"""
from __future__ import annotations

import hashlib
import re
import sys

from sayfalar import KOK, sayfalar

STIL = KOK / "assets" / "site.css"

# href="/assets/site.css" ya da href="/assets/site.css?v=eskidamga"
DESEN = re.compile(r'href="/assets/site\.css(?:\?v=[0-9a-f]+)?"')


def damga() -> str:
    return hashlib.sha256(STIL.read_bytes()).hexdigest()[:10]


def yaz(kontrol: bool) -> int:
    v = damga()
    yeni_ref = f'href="/assets/site.css?v={v}"'
    bayat: list[str] = []
    yazilan = 0

    for f in sayfalar():
        metin = f.read_text(encoding="utf-8")
        if not DESEN.search(metin):
            continue
        guncel = DESEN.sub(yeni_ref, metin)
        if guncel == metin:
            continue
        if kontrol:
            bayat.append(str(f.relative_to(KOK)))
        else:
            f.write_text(guncel, encoding="utf-8")
            yazilan += 1

    if kontrol:
        if bayat:
            print(f"stil damgası BAYAT ({len(bayat)} sayfa), beklenen ?v={v}")
            for b in bayat[:8]:
                print("  " + b)
            print("Düzeltmek için: python3 tools/assets.py")
            return 1
        print(f"stil damgası güncel (?v={v}).")
        return 0

    print(f"stil damgası yazıldı: ?v={v} — {yazilan} sayfa güncellendi.")
    return 0


if __name__ == "__main__":
    sys.exit(yaz("--check" in sys.argv))
