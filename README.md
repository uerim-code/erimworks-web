# erimworks-web

erimworks.com için statik site (şimdilik placeholder) + AdMob `app-ads.txt`.

## app-ads.txt
Tüm uygulamalar tek AdMob hesabı (pub-4453331627814444) altında → tek yetkili satıcı satırı.
Mediation eklendikçe her ağ için ek satır girilecek.

## CSP

`_headers` içindeki `Content-Security-Policy` satırı ÜRETİLİR, elle yazılmaz:
politika sayfalardaki satır içi betikleri sha256 ile adlandırıyor.

```
python3 tools/csp.py           # _headers'ı güncelle
python3 tools/csp.py --check   # bayatsa 1 ile çık
```

**Bir satır içi betiği değiştirdikten sonra bunu çalıştır.** Çalıştırılmazsa
hash tutmaz, tarayıcı betiği sessizce bloklar ve hiçbir hata görünmez. Bu
sitede en pahalı kayıp gizlilik/destek sayfalarındaki dil seçicidir — o
sayfalar mağaza uyum yüzeyi.

## Sitemap

`sitemap.xml` de ÜRETİLİR: canonical'ı kendini gösteren, noindex olmayan ve
hukuki/destek olmayan sayfalar girer; `lastmod` dosyanın son commit tarihidir.

```
python3 tools/sitemap.py           # sitemap.xml'i yaz
python3 tools/sitemap.py --check   # adres kümesi bayatsa 1 ile çık
```

Yeni bir sayfa ekledikten ya da bir sayfayı değiştirdikten sonra çalıştır.

## Fontlar

Sora ve Plus Jakarta Sans, Google Fonts'tan değil `/assets/fonts/` altından
sunulur (`@font-face` kuralları `assets/site.css`'in başında; değişken woff2,
yalnız latin + latin-ext). Sebep: fonts.googleapis.com'dan gelen CSS render'ı
bloklayıp LCP'yi geciktiriyordu ve CSP'de iki 3. taraf origin gerektiriyordu.
Yeni ağırlık gerekirse `font-weight` aralığı zaten 400–700 (Sora) / 400–600
(Plus Jakarta Sans); yeni alt küme gerekirse Google'ın css2 ucundan woff2
indirip aynı kalıpla ekle.

## AI / GEO dosyaları

- `llms.txt`: AI arama motorları için site özeti (elle yazılır; yeni ürün
  eklenince güncelle).
- `robots.txt`: tüm AI botlarına açık, `Content-Signal` tercih satırı var.
- `.well-known/security.txt`: güvenlik iletişimi; `Expires` yılda bir uzatılır
  (son: 2027-11-03).
- Ana sayfa ve ürün sayfalarındaki JSON-LD, `https://erimworks.com/#org` ve
  `#founder` kimliklerine `@id` ile bağlanır; yeni sayfa eklerken aynı
  `@id`'leri kullan, `publisher`'ı satır içi yeniden tanımlama.
