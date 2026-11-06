#!/usr/bin/env python3
"""_headers dosyasındaki Content-Security-Policy satırını üretir.

    python3 tools/csp.py            # _headers'ı güncelle
    python3 tools/csp.py --check    # bayatsa 1 ile çık (yayın öncesi kapı)

NEDEN ÜRETİLİYOR, ELLE YAZILMIYOR: politika satır içi betikleri sha256 ile
adlandırıyor. Bir betiğin TEK KARAKTERİ değişirse hash tutmaz ve tarayıcı o
betiği SESSİZCE bloklar — konsola bakan olmadığı sürece hiçbir belirti yok.
Bu sitede en çok bunu kaybetmek acıtır: gizlilik/destek sayfalarındaki DİL
SEÇİCİ satır içi bir betiktir ve o sayfalar mağaza uyum yüzeyidir.

⚠ JSON-LD blokları BİLEREK hash'lenmiyor. `application/ld+json`
çalıştırılabilir bir betik değildir; `script-src` onu bloklamaz. Tarayıcıda
ölçüldü: hash'i tutmayan bir CSP altında satır içi JS bloklandı, JSON-LD
öğesi DOM'da kaldı, içeriği okunabilirdi ve ona dair ihlal ÇIKMADI.
Hash'lenseydi her sayfanın kendi JSON-LD'si için ayrı hash gerekirdi.

⚠ `style-src` içinde 'unsafe-inline' VAR ve bu kaçınılmaz: sayfalarda 100'ü
aşkın `style="..."` özniteliği var, öznitelik stilleri hash'lenemez. Stil
enjeksiyonu kod çalıştırmaz, bu yüzden takas kabul edildi.
"""
from __future__ import annotations

import base64
import hashlib
import re
import sys

from sayfalar import KOK, sayfalar

# Ölçülen dış yükler (2026-09-02). Sayfalardaki diğer https adreslerinin hepsi
# <a href> — CSP bağlantıları kısıtlamaz, yalnız YÜKLENEN kaynağı kısıtlar.
# Fontlar 2026-11-03'ten beri /assets/fonts/ altında kendi sunucumuzda; Google
# Fonts origin'leri politikadan çıkarıldı (render-blocking dış CSS + 3. taraf).
# testroster/index.html bekleme listesi kaydını buraya POST ediyor.
TESTROSTER_API = "https://iebavqhqsldsxjmiquhy.supabase.co"

# ⚠ CLOUDFLARE WEB ANALYTICS — DEPODA İZİ YOK. Beacon betiğini Cloudflare
# KENAR SUNUCUDA yanıta enjekte ediyor, yani HTML kaynağını tarayarak
# bulunamaz. İlk CSP sürümü tam da bu yüzden onu bloklamıştı: politika
# depodaki dosyalar ölçülerek yazılmıştı ve bu betik orada yok. Canlı sayfayı
# tarayıcıda açınca ihlal görüldü.
#
# Ders: bu sitenin CSP'si yalnız kaynaktan ölçülerek doğrulanamaz. Değiştiren
# kişi CANLI sayfayı tarayıcı konsoluyla da açmalı.
CF_BEACON = "https://static.cloudflareinsights.com"
CF_RUM = "https://cloudflareinsights.com"

SCRIPT_DESENI = re.compile(r"<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>", re.S)


def hashler() -> list[str]:
    bulunan: set[str] = set()
    # Sayfa listesi tools/sayfalar.py'den: yalnız git'in takip ettiği, yani
    # YALNIZ yayına giden dosyalar. Daha önce burada elle bir dışlama listesi
    # vardı ({node_modules, reports, .claude}); sorun şu ki yoksayılan her yeni
    # klasör o listeye ayrıca yazılmadıkça politikaya sızıyor.
    for f in sayfalar():
        for oz, govde in SCRIPT_DESENI.findall(f.read_text(encoding="utf-8", errors="replace")):
            if "ld+json" in oz:
                continue
            d = hashlib.sha256(govde.encode("utf-8")).digest()
            bulunan.add("'sha256-" + base64.b64encode(d).decode() + "'")
    return sorted(bulunan)


def politika() -> str:
    return "; ".join([
        "default-src 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "form-action 'self'",
        "script-src 'self' " + " ".join(hashler()) + f" {CF_BEACON}",
        "style-src 'self' 'unsafe-inline'",
        "font-src 'self'",
        "img-src 'self' data:",
        f"connect-src 'self' {TESTROSTER_API} {CF_RUM}",
        "upgrade-insecure-requests",
    ])


def yaz(kontrol: bool) -> int:
    yol = KOK / "_headers"
    metin = yol.read_text(encoding="utf-8")
    satir = f"  Content-Security-Policy: {politika()}"

    if re.search(r"^  Content-Security-Policy: .*$", metin, re.M):
        yeni = re.sub(r"^  Content-Security-Policy: .*$", lambda _: satir, metin, count=1, flags=re.M)
    else:
        # /* bloğunun son güvenlik başlığından hemen sonra.
        capa = "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
        if capa not in metin:
            raise SystemExit("_headers beklenen biçimde değil: HSTS satırı bulunamadı.")
        yeni = metin.replace(capa, capa + satir + "\n", 1)

    if kontrol:
        if yeni != metin:
            print("_headers BAYAT: CSP satırı sayfalardaki betiklerle uyuşmuyor.")
            print("Düzeltmek için: python3 tools/csp.py")
            return 1
        print(f"_headers güncel ({len(hashler())} betik hash'i).")
        return 0

    yol.write_text(yeni, encoding="utf-8")
    print(f"_headers yazıldı — {len(hashler())} betik hash'i.")
    return 0


if __name__ == "__main__":
    sys.exit(yaz("--check" in sys.argv))
