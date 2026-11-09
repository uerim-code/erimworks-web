#!/usr/bin/env python3
"""Sayfalardaki JSON-LD bloklarını ayrıştırır ve iki sessiz kusuru yakalar.

    python3 tools/jsonld.py            # bulguları yaz
    python3 tools/jsonld.py --check    # kusur varsa 1 ile çık (yayın kapısı)

NEDEN VAR — JSON-LD BOZULUNCA KİMSE DUYMAZ. Blok sayfanın görünüşünü hiç
etkilemez: virgülü eksik bir yapılandırılmış veri bloğu tarayıcıda hatasız
açılan, Google'da ise hiç görünmeyen bir sayfa üretir. Elle düzenlenen bir
alanda bunun olması an meselesi — bu depoda SSS blokları hem JSON-LD'de hem
görünür `<details>` içinde, yani aynı metin iki yerde duruyor.

İKİ KONTROL:

1. **Ayrıştırılabilirlik.** Her `application/ld+json` bloğu geçerli JSON mu.

2. **SSS'nin sayfada karşılığı var mı.** `FAQPage` içinde bildirilen her
   sorunun sayfanın GÖRÜNÜR metninde bir karşılığı olmalı; Google'ın kuralı
   yapılandırılmış verinin sayfadaki içeriği temsil etmesidir. Sayfada olmayan
   bir soruyu bildirmek ihlaldir. 2026-11-08'de dört sayfaya birden SSS
   eklendi — elle korunan her eşleşme bir gün elle bozulur.

   ÖLÇÜ KELİME ÖRTÜŞMESİDİR, BİREBİR METİN DEĞİL — ölçüldü: ilk hâli
   `<summary>` sayısını sayıyordu ve `astrorota/index.html`i yanlışlıkla
   suçladı; o sayfa SSS'yi `<details>` ile değil `<h3>` ile gösteriyor.
   Birebir metin karşılaştırması da yanlış alarm verirdi: aynı sayfada
   JSON-LD "Retro gölge dönemi nedir?" derken başlık "Retro **ve** gölge
   dönemi nedir?" diyor. İşaretleme biçimi ve küçük sözcük farkları kusur
   değildir; sorunun sayfada hiç karşılığı olmaması kusurdur.

HREFLANG.PY İLE İŞ BÖLÜMÜ — ikisi aynı şeye bakmıyor:

  hreflang.py → yalnız TR/EN **çiftlerinde** (18 sayfa), ama ORADA KATI:
                şema ile görünür `<details>` metni BİREBİR aynı olmalı.
  jsonld.py   → **bütün** yayın sayfalarında (84), ama orada GEVŞEK: yalnız
                sorunun sayfada bir karşılığı var mı.

Yani tek dilli sayfalar (TestRoster, AstroRota, uygulama sayfaları) hreflang
denetiminin dışında kalıyor; bu dosya o boşluğu kapatıyor. Çiftlerde katı
kontrolü hreflang.py yaptığı için burada tekrarlanmıyor.

Yalnız yayına giden sayfalara bakar (`sayfalar.py`).
"""
from __future__ import annotations

import json
import re
import sys

from sayfalar import sayfalar

BLOK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
ETIKET = re.compile(r"<[^>]+>")
KELIME = re.compile(r"\w+", re.UNICODE)

# Sorunun kelimelerinin en az bu oranı sayfa metninde geçmeli.
ESIK = 0.7


def govde(metin: str) -> str:
    """Sayfanın görünür metni — betikler ve stil blokları çıkarılmış."""
    g = re.sub(r"<script.*?</script>|<style.*?</style>", " ", metin, flags=re.S)
    return ETIKET.sub(" ", g).casefold()


def denetle() -> list[str]:
    kusurlar: list[str] = []
    for yol in sayfalar():
        metin = yol.read_text(encoding="utf-8")
        gorunur = govde(metin)
        for i, ham in enumerate(BLOK.findall(metin)):
            try:
                veri = json.loads(ham)
            except json.JSONDecodeError as hata:
                kusurlar.append(f"{yol}: blok {i} ayrıştırılamadı — {hata}")
                continue
            for dugum in veri.get("@graph", [veri]):
                if not isinstance(dugum, dict) or dugum.get("@type") != "FAQPage":
                    continue
                for soru in dugum.get("mainEntity", []):
                    ad = soru.get("name", "")
                    kelimeler = [k.casefold() for k in KELIME.findall(ad)]
                    if not kelimeler:
                        continue
                    gecen = sum(1 for k in kelimeler if k in gorunur)
                    if gecen / len(kelimeler) < ESIK:
                        kusurlar.append(
                            f"{yol}: FAQPage sorusu sayfada görünmüyor — {ad!r} "
                            f"({gecen}/{len(kelimeler)} kelime)"
                        )
    return kusurlar


def main(kontrol: bool) -> int:
    kusurlar = denetle()
    if kusurlar:
        for k in kusurlar:
            print(k)
        if kontrol:
            return 1
        return 1
    print(f"JSON-LD temiz ({len(sayfalar())} sayfa).")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
