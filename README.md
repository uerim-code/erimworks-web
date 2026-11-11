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

## Stil damgası (cache-busting)

`/assets/site.css` adresinin sonundaki `?v=` damgası ÜRETİLİR: CSS'in kendi
sha256'sının ilk on hanesi.

```
python3 tools/assets.py           # damgayı güncelle
python3 tools/assets.py --check   # bayatsa 1 ile çık
```

**CSS'i her değiştirdikten sonra bunu çalıştır.** Çalıştırılmazsa değişiklik
ziyaretçiye ULAŞMAZ ve hiçbir hata görünmez: `_headers` `/assets/*` için yedi
günlük önbellek veriyor, Cloudflare adrese göre önbelleğe alıyor ve Pages'e
dağıtım kenar sunucudaki eski nesneyi düşürmüyor. 2026-11-06'da ölçüldü —
canlı sitede HTML yeniydi, CSS beş günlüktü (`age: 435322`, `cf-cache-status:
HIT`): taze işaretleme, henüz var olmayan sınıflara atıf.

Damga sayesinde `/assets/*` için uzun önbellek artık doğru: adres içerikle
birlikte değişiyor.

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

## IndexNow

Kök dizindeki `e5711a3b8b16fb65709daa31e9f39703.txt` IndexNow anahtar dosyasıdır (içeriği dosya adıyla
aynı; herkese açık olması tasarım gereği). Bing, Yandex, Naver ve Seznam bu
protokolü okur; ChatGPT araması Bing dizinine dayandığı için önemlidir.
Yayından sonra değişen adresleri bildirmek için:

```
curl -s -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json; charset=utf-8' \
  -d '{"host":"erimworks.com","key":"e5711a3b8b16fb65709daa31e9f39703","keyLocation":"https://erimworks.com/e5711a3b8b16fb65709daa31e9f39703.txt","urlList":["https://erimworks.com/","https://erimworks.com/hakkimizda/"]}'
```

Yanıt 200 ya da 202 ise kabul edildi. Cloudflare panelinde Caching → Crawler
Hints açıksa Cloudflare da aynı protokolle otomatik bildirim yapar.

## İngilizce sayfalar ve hreflang

Ana sayfa ve altı B2B sayfanın İngilizce sürümü `en/` altında ayrı adreslerdir
(`/` ↔ `/en/`, `/unvportal/sinav/` ↔ `/en/unvportal/exams/` vb.). TR ve EN
sayfalar birbirini `<link rel="alternate" hreflang>` ile gösterir; x-default TR.
Dil seçici artık bağlantıdır, ana sayfadaki `data-tr`/`data-en` takası kaldırıldı.

```
python3 tools/hreflang.py      # çiftler, JSON-LD ve SSS eşleşmesi; sorun varsa 1
```

**Bir çiftin tek tarafını değiştirince bunu çalıştır.** EN sayfa yazarken ürün
`@id`'si TR köküyle aynı kalır (`https://erimworks.com/unvportal/#app`); yalnız
`WebPage` düğümü `/en/` altındadır.

## Yapılandırılmış veri (JSON-LD)

```
python3 tools/jsonld.py           # bulguları yaz
python3 tools/jsonld.py --check   # kusur varsa 1 ile çık
```

İki şeye bakar: her `application/ld+json` bloğu geçerli JSON mu, ve `FAQPage`
içinde bildirilen her sorunun sayfanın görünür metninde bir karşılığı var mı.
`hreflang.py` ile iş bölümü: o yalnız TR/EN çiftlerinde ama orada **birebir**
eşleşme arar; bu dosya bütün yayın sayfalarında ama yalnız "sayfada karşılığı
var mı" diye bakar. Tek dilli sayfalar (TestRoster, uygulama sayfaları)
hreflang denetiminin dışında kaldığı için bu boşluk ayrıca kapatıldı.

## Yayın kapısı (git hook)

Yukarıdaki beş aracın hiçbiri kendiliğinden çalışmıyordu; hepsi "değişiklikten
sonra şunu çalıştır" notuna bağlıydı. `.githooks/pre-commit` bunu bir kapıya
çevirir: hazırlanan dosyalar arasında `.html` ya da `.css` varsa `csp`,
`assets`, `sitemap`, `jsonld` ve `hreflang` kontrolleri koşar, biri bayatsa
commit durur. Yaklaşık bir saniye sürer.

```
git config core.hooksPath .githooks   # yeni klonda bir kez
git commit --no-verify                # tek seferlik atlamak için
git config --unset core.hooksPath     # tamamen kapatmak için
```

**Neden gerekti — ölçüldü (2026-11-08):** aynı oturumda dört sayfaya SSS
eklenirken iki tanesinde şema ile görünür metin ayrıştı (şemada "ÖNİZLEME",
sayfada "önizleme"). `hreflang.py` bunu yakalayabilirdi ama kimse
çalıştırmamıştı; kusur ancak araçlar tek tek elden geçirilirken görüldü.

## Çerez rızası ve ölçüm

Ölçüm Google Tag Manager (`GTM-TPV949ZK`) ile yapılır ve **yalnız ziyaretçi
kabul ederse yüklenir**. Mantık `assets/cerez.js` içinde; satır içi betik yok,
yani CSP hash'i gerektirmez.

```
python3 tools/cerez.py           # betiği her sayfaya koy / damgayı tazele
python3 tools/cerez.py --check   # eksik ya da bayatsa 1 ile çık
```

Davranış, ölçülerek doğrulandı (2026-11-11, yerel tarayıcı):

| Durum | GTM betiği | Çerez |
|---|---|---|
| Karar verilmemiş | yüklenmez | yok |
| Reddedildi | yüklenmez | yok |
| Kabul edildi | yüklenir | `_ga`, `_ga_*` |

Google'ın önerdiği Consent Mode v2'de GTM her zaman yüklenir ve rıza yokken
çerezsiz ping gönderir; burada o yol **seçilmedi**. "Reddet"e basan
ziyaretçinin tarayıcısından Google'a hiçbir istek gitmemesi savunması kolay
tek davranış. Reklam kişiselleştirmesi ve reklam kullanıcı verisi ise her
durumda kapalı — kabul edilse bile.

Rıza kararı `localStorage`da `ew-cerez` anahtarında durur; bunun için çerez
kullanılmaz. Gizlilik sayfasındaki "Çerez tercihimi değiştir" düğmesi kararı
sıfırlar (`data-cerez-ayar` özniteliği taşıyan herhangi bir öge çalışır).

**Metin değişirse `SURUM` sabitini artır** — eski rızalar geçersizleşir ve
bant yeniden sorulur. Kapsam genişlediğinde (yeni bir ölçüm aracı) bu
zorunludur: eski rıza yeni kapsamı karşılamaz.
