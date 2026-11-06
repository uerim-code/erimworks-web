# Ürün gerçekleri — erimworks.com metninin kanıt tabanı

Bu klasördeki her dosya **ürünün kendi deposundan** çıkarıldı: rotalar, ekranlar,
veritabanı modelleri, API uçları, faz/durum belgeleri. Amaç tek: siteye yazılan her
iddianın bir dosya yolu karşılığı olsun.

**Neden gerekli.** Daha önce Labs sayfası üründe karşılığı olmayan özellikler
anlatıyordu ve ana sayfa "RLS" diye bir kısaltmayı satış argümanı sanıyordu. Metin iyi
yazılmıştı, sadece doğru değildi. Kurumsal alıcı demoda ilk o maddeyi sorar.

## Dosyalar

| Ürün | Dosya | Kaynak depo |
|---|---|---|
| UNVPortal Labs | `unvportal-labs.md` | `unvportal/unvportal` (FastAPI + lab-frontend) |
| UNVPortal Exams | `unvportal-exams.md` | `unvportal/unvportal` + `unvportal-sinav-*` |
| UNVPortal Quality | `unvportal-quality.md` | `unvportal/unvplatform` (monorepo) |
| International Patient OS | `international-patient-os.md` | `international-patient-os` |
| KursOS | `kursos.md` | `merkur-saas` + `kursos-mobile` |
| TestRoster | `testroster.md` | `testroster` |
| ChemBioCalc | `chembiocalc.md` | `chemcalc-pro` |

## Taramanın üç ana bulgusu

**1. Site ürünleri olduğundan küçük gösteriyor.** En uç örnek Quality: site dört
kelimeyle anlatıyor (*kanıt toplama, komisyon ve karar takibi, PUKÖ, iç değerlendirme
raporu*), ürün 157 sayfa ve 50+ modül — CAPA, risk, mevzuat izleme, iç denetim,
gösterge takibi, OCR, veri odası, SSO, bağlayıcılar, mobil uygulama. Aynı durum
IPOS (dikte, çeviri, hasta portalı, kiracıya özel alan adı sitede yok) ve
TestRoster (Production Readiness Score, dropout riski, otomatik yerine tester yok) için
de geçerli.

**2. İki ürün arasındaki en güçlü bağ hiç anlatılmamış.** ChemBioCalc'ın `app/lab/`
bölümü UNVPortal Labs'ın saha uygulaması: cihaz QR'ını okut, rezervasyonu/stoğu/
yoklamayı cihaz başında yap. Labs tarafındaki karşılığı `CihazEnvanteri.qr_token`.
"Aynı ekosistem" iddiasının tek somut kanıtı bu ve sitede yok.

**3. Depoların kendi belgeleri de yanıltıyor.** TestRoster'ın README'si "uygulamalar
henüz iskelet" diyor; `docs/FAZ-DURUM.md` 40 fazın çoğunu "bitti" gösteriyor.
Labs'ın uygulama içi kullanım kılavuzu "kalibrasyon tarihleri" diyor; `CihazEnvanteri`
modelinde kalibrasyon alanı yok. Kaynak olarak koda bakıldı, belgelere değil.

## Kullanım

Metin yazan her skill (copywriting, landing-page-copy, content-strategy, aso…) işe
başlarken ilgili ürünün dosyasını okur. Bir iddia dosyada **İDDİA EDİLMEMESİ
GEREKENLER** başlığı altındaysa metne girmez. Dosyada olmayan bir iddia yazılacaksa
önce koddan doğrulanır ve buraya eklenir.

Her dosyanın sonunda **Açık sorular** var: bunlar koddan çıkmaz, Ümit'in yanıtlaması
gerekir (kaç kurum kullanıyor, hangi modül müşteride açık, hangi nesil satılıyor).

**Tarama tarihi: 2026-11-06.** Ürün deposu değiştiğinde ilgili dosya yenilenir.
