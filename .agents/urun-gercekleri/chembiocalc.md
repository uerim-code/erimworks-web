# ChemBioCalc — ürün gerçeği

**Kaynak:** `~/projects/chemcalc-pro` (Expo/RN uygulama + `apps/web` statik site).
Son commit: 2026-11-06 (bugün). **Tarama tarihi:** 2026-11-06.
Web sitesi `chembiocalc.com` → kaynak `chemcalc-pro/apps/web/public`
(`chembiocalc-web` deposu bayat kopyadır, orada çalışılmaz).

## Ölçü

- **40 kimya hesaplayıcı** (`app/chemistry/*.tsx`)
- 117 ekran dosyası toplam
- **52 web sayfası** (`apps/web` altında her biri ayrı hesaplayıcı/landing)
- Sekmeler: ana sayfa, **defter (notebook)**, **kronometre (timer)**

## Doğrulanmış hesaplayıcılar (örnekler)

Arrhenius, denklem denkleştirme (balancer), tampon hazırlama, kromatografi,
derişim çevirici, **DOE (deney tasarımı)**, elektrokimya, elektroliz, ampirik formül,
**Gage R&R**, gaz yasaları, GC, jel analizi, yeşil kimya metrikleri, **HPLC kolon
seçici / gradyan / metot transferi / sekans oluşturucu**, çıkarım (inference),
izotermler, kinetik, Ksp, kütle spektrometrisi, **metot doğrulama**, molekül,
çok bileşenli UV…

Web tarafında ayrıca: ELISA 4PL, hücre ekimi, qPCR standart eğrisi, Fe3O4 nanopartikül
sentezi, karbon kuantum nokta, molarite, tampon hazırlama, HPLC mobil faz.

## SİTENİN KAÇIRDIĞI EN BÜYÜK HİKÂYE

`app/lab/` altında **UNVPortal Labs köprüsü** var (`lib/unvportal.ts` — kimlik köprüsü
ve zaman aşımlı istemci). Ekranlar: **tara (QR), rezervasyon, stok, yoklama, onaylar,
sonuç**.

Yani ChemBioCalc yalnız bir hesap makinesi değil: **UNVPortal Labs'ın saha uygulaması**.
Laboratuvar personeli cihazın QR etiketini telefonla okutup rezervasyonu, stok
düşümünü ve yoklamayı cihaz başında yapıyor. Labs tarafındaki karşılığı
`CihazEnvanteri.qr_token` (benzersiz, dizinli).

Site şu an ChemBioCalc'ı "laboratuvar hesaplayıcıları" diye tek satırla geçiyor ve bu
bağı hiç kurmuyor. Oysa iki ürünü birbirine bağlayan, kurumsal alıcıya "aynı
ekosistem" diyen tek somut kanıt bu.

## Para ve dağıtım

- Abonelik altyapısı: `lib/purchases.ts`, `entitlements.ts`, `storeOffers.ts`,
  `paddleSignature.ts` (hem mağaza hem Paddle)
- Reklam: AdMob entegrasyonu portföy kuralına göre
- Son commit bugün: *"Sistem uygunluğu ücretsiz: yayın denetimi listesi, uygulama web
  köprüsü (webKapili false), ana sayfa yenilik kartı"* — ücretsiz/ücretli sınırı
  aktif olarak değişiyor; metne fiyat/kapı yazılmadan önce o günkü hâli doğrulanmalı.

## İDDİA EDİLMEMESİ GEREKENLER

- Hesaplayıcıların bilimsel doğruluğu depoda ayrı bir açık başlık:
  `SCIENTIFIC-REVIEW-REQUIRED.md` dosyası var. "Doğrulanmış/akredite hesaplama"
  türü iddia bu dosya kapanmadan yazılmamalı.
- Lab köprüsü yalnız UNVPortal kurulumu olan kurumda çalışır; bağımsız kullanıcıya
  "laboratuvarını yönet" denmemeli.

## Açık sorular

- 40 hesaplayıcının kaçı ücretsiz, kaçı abonelik arkasında (bugün değişti)?
- Lab köprüsü hangi UNVPortal sürümüyle uyumlu — eski `unvportal` mı, `unvplatform` mı?
