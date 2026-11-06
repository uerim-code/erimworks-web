#!/usr/bin/env python3
"""Sitenin YAYINA GİDEN HTML sayfalarını listeler. Tek tanım, iki araç.

Cloudflare Pages deponun kendisini dağıtır. Dolayısıyla "sitenin sayfası"nın
tek doğru tanımı şudur: **git'in takip ettiği .html dosyası.** Depoda duran
ama yoksayılan her şey (denetim anlık görüntüleri, araç çıktıları) yayına
gitmez, bu yüzden hiçbir aracın onlara bakması doğru değil.

NEDEN AYRI BİR DOSYA — ÖLÇÜLDÜ: 2026-11-06'da iki araç bu tanımı ayrı ayrı
yazdığı için ikisi de yanlış yerlere baktı:

  csp.py     → `reports/geo-raw/homepage.html` içindeki satır içi betiğin
               hash'ini ÜRETİM CSP'sine ekliyordu. Yayına hiç gitmeyen bir
               dosya, canlı politikada fazladan bir betiğe izin veriyordu
               (9 hash sayılmıştı, sitenin ihtiyacı 8).
  assets.py  → aynı anlık görüntülere damga basıp denetim kaydını bozuyordu.

Tanım tek yerde durursa iki araç bir daha ayrışamaz.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent

# git yoksa geri düşülecek liste: yoksayılan, yayına gitmeyen üst klasörler.
YAYIN_DISI = {"reports", "node_modules", ".taste-skill", ".impeccable", ".git"}


def sayfalar() -> list[pathlib.Path]:
    try:
        ham = subprocess.run(
            ["git", "-C", str(KOK), "ls-files", "-z", "*.html"],
            capture_output=True, check=True, timeout=20,
        ).stdout
        yollar = [KOK / p for p in ham.decode().split("\0") if p]
        if yollar:
            return sorted(yollar)
        raise RuntimeError("git hiç .html döndürmedi")
    except Exception as e:  # git yok, depo değil, ya da boş sonuç
        print(f"uyarı: git sorulamadı ({e}); klasör taramasına düşülüyor.", file=sys.stderr)
        return sorted(
            f for f in KOK.rglob("*.html")
            if not (YAYIN_DISI & set(f.relative_to(KOK).parts))
        )


if __name__ == "__main__":
    for f in sayfalar():
        print(f.relative_to(KOK))
