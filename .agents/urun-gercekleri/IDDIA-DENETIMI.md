# İddia denetimi — site metni ⟷ ürün kodu

**Tarih:** 2026-11-06. **Yöntem:** sitedeki iddialar `.agents/urun-gercekleri/`
dosyalarına ve doğrudan ürün koduna karşı tek tek denetlendi.
**Kapsam:** ana sayfa, `unvportal/` (hub + labs + sinav + kalite), `hakkimizda/`,
`saglik-turizmi/`, `kurs-yonetim/`, `chembiocalc/`, `testroster/` ve EN karşılıkları.

Hükümler: **DESTEKLENEN** · **YANLIŞ** · **DOĞRULANAMADI** · **EKSİK** (doğru ama sitede yok)

---

## 1. YANLIŞ — "Üç modül aynı veritabanını paylaşır" (11 sayfa)

Sitenin omurga iddiası bu. Geçtiği yerler:

`index.html` (hero + sayı bandı üstü + platform bandı), `unvportal/index.html`
(üç ayrı yerde, ayrıca **"Tek veritabanının pratik karşılığı"** diye başlı bütün bir
bölüm), `unvportal/labs/index.html`, `unvportal/sinav/index.html`,
`hakkimizda/index.html` ve EN karşılıkları (`en/index`, `en/unvportal/index`,
`en/unvportal/labs`, `en/about`).

Örnek cümleler:
- *"Labs, UNVPortal Exams ve UNVPortal Quality ile aynı veritabanını paylaşır."*
- *"Birlikte kullanıldıklarında birim, personel ve yetki tanımları tek veritabanından okunur."*
- *"…laboratuvar, sınav, kalite ve akreditasyon süreçlerini tek veritabanı üzerinde yürüten…"*

### Kodun söylediği

**Labs ↔ Exams: DOĞRU.** `unvplatform/apps/platform-api/src/openapi.ts`:
> *"UnvPortal ve Sınav Otomasyonu (**AYNI** api.unvportal.com; sınav = `/api/v2/sinav-oto/*` uç grubu)"*

İkisi de `~/projects/unvportal/unvportal/backend` altında tek FastAPI + tek
`DATABASE_URL`. Bu kısım doğrulandı.

**Quality: YANLIŞ.** Quality ayrı bir sistemdir:
- Ayrı depo/monorepo: `unvportal/unvplatform`
- Ayrı şema: `apps/platform-api/prisma/schema.prisma` — **508 model**, içinde tek bir
  cihaz/numune/sınav tablosu yok
- Ayrı adres: `platform-api.unvportal.com` / `quality.unvportal.com`

Ve ürünün kendi OpenAPI etiketi, aynı dosyada, iddianın tam tersini söylüyor:
> *"Legacy entegrasyonu — **YALNIZ OKUNUR: legacy VERİTABANINA bağlanılmaz,
> legacy'ye YAZILMAZ → mevcut sistemler bağımsız çalışır.** Secret düz metin
> saklanmaz; gereksiz öğrenci PII'si KOPYALANMAZ (allow-list + maskeleme);
> her üretilen Quality kaydı için kaynak sisteme LINEAGE izi."*

Yani Quality, Labs/Exams verisini **API üzerinden, yalnız okuyarak, maskeleyerek ve
izini sürerek** alıyor. Paylaşılan bir veritabanı yok.

### Neden önemli

İddia yalnız yanlış değil, **gerçeğinden zayıf**. Kurumsal alıcının korkusu
"yeni yazılım çalışan sistemimi bozar mı" sorusudur. Ürünün gerçek cevabı tam da
bunu karşılıyor: *mevcut sistemler bağımsız çalışır, Quality hiçbir şey yazmaz,
her kayıt kaynağına kadar izlenir.* Site bunu "aynı veritabanı" diye anlatarak hem
yanlış söylüyor hem elindeki en güçlü güvence argümanını harcıyor.

### Ne yapılmalı

- Labs+Exams için "aynı sistem / aynı veritabanı" kalabilir.
- Quality'nin geçtiği her cümle yeniden yazılmalı: *"Quality, Labs ve Exams
  kayıtlarını yalnız okuyarak kanıt olarak kullanır; mevcut sistemlere hiçbir şey
  yazmaz ve her kanıtın kaynağı izlenir."*
- Fonksiyonel vaat (**"aynı bilgi ikinci kez girilmez"**) ayakta kalıyor — mekanizma
  değişiyor, sonuç değil.
- `unvportal/index.html`'deki **"Tek veritabanının pratik karşılığı"** bölümü
  bütünüyle elden geçmeli.

---

## 2. Labs sayfası — madde madde

| İddia | Hüküm | Kanıt |
|---|---|---|
| "Her öğrenciye QR etiketli ayrı numune; gerçek değer ve kabul toleransı önceden tanımlı" | **DESTEKLENEN** | `models_v2.py: Numune` — `qr_token`, `gercek_deger`, `tolerans_mutlak`, `tolerans_yuzde`, `analit_turu` |
| "Cihazlar konum, çalışma saatleri, günlük/saatlik rezervasyon moduyla tanımlanır; bakım günleri müsait değil işaretlenir" | **DESTEKLENEN** | `AnalitikCihaz`: `konum`, `calisma_baslangic/bitis`, `rezervasyon_modu` ("gunluk"/"saatlik"), `musait_olmayan_tarihler` |
| "Anabilim dalı için paylaşılabilir bağlantı; kurum dışından talep alınır" | **DESTEKLENEN** | `rezervasyon.py: POST /talep` (kimliksiz) + `CihazRezervasyon`: `ad_soyad`, `email`, `kurum`, `telefon` |
| "Tek tek ya da toplu onaylanır, reddedilirse gerekçesi kaydedilir" | **DESTEKLENEN** | `/admin/rezervasyon/{id}/onayla`, `/reddet`, `/admin/toplu-onayla`, `/admin/toplu-duzenle-onayla`; `red_nedeni` alanı |
| "Randevu öncesi hatırlatma otomatik gider" | **KISMEN — DÜZELTİLDİ 2026-11-08** | Uçlar var (`/hatirlatma`, `/admin/hatirlatma-gonder`, **`/hatirlatma-cron`**) ve mail servisi bağlı. "Otomatik" olması cron'un kurulumda zamanlanmasına bağlı — ürün özelliği değil kurulum adımı. Metin "hatırlatma gönderilir" demeli ya da kurulum notu düşmeli. |
| "Dönem sonunda cihaz başına kullanım raporu" | **DESTEKLENEN** | `/admin/rapor`, `/admin/rezervasyon/{id}/kullanim` |
| "Kritik seviyenin altına düşen malzeme listelenir" | **DESTEKLENEN** | `CamSarf.kritik_adet`, `Kimyasal.kritik_miktar` |
| "Tüketim geçmişi satın alma planı için dışa aktarılır" | **DESTEKLENEN** | `stok.py` → `satin_alma_listesi.xlsx` |
| "Lot ve son kullanma tarihi olan malzemelerde süresi geçenler ayrılır" | **DESTEKLENEN (dar)** | `KimyasalKap`: `lot_no`, `son_kullanma_tarihi`, `acilis_tarihi`. **Yalnız kimyasal kaplarında** — cam/sarf tarafında lot/SKT alanı yok. Cümle "olan malzemelerde" dediği için doğru, ama okuyan bunu sarf için de sanabilir. |
| SSS: "Elektronik tablo halindeki cihaz, sarf ve laboratuvar listeleri kurulum sırasında içe aktarılıyor" | **DESTEKLENEN — bu denetim ilk turda YANILDI** | İlk tarama `stok.py`'de içe aktarma ucu bulamamıştı; 2026-11-08'de yeniden bakıldığında **üç uç** çıktı: `POST /stok/import/cihaz` (s. 895), `/stok/import/cam-sarf` (s. 936), `/stok/import/kimyasal` (s. 980) — openpyxl ile, başlık satırından sütun eşlemeli. Arayüzde de var: `StokYonetimiPage.jsx` üç yerde "Excel Yükle" düğmesi (`.xlsx,.xls`). Yani özellik **sitenin anlattığından geniş**: kurulumla sınırlı değil, yetkili kullanıcı istediği zaman yükleyebiliyor. Site metni buna göre genişletildi. |
| "Tarayıcı üzerinden çalışır, bulut ya da kendi sunucusu" | **DESTEKLENEN** | web uygulaması; dağıtım kararı kurumun |
| "Yetkiler birim ve rol bazında; sorumlu yalnız kendi laboratuvarını görür" | **DESTEKLENEN** | `anabilim_dali_id` bağları + `alembic/versions/014_rls_public_tablolar.py` |

---

## 3. Diğer sayfalar

| Sayfa / iddia | Hüküm | Not |
|---|---|---|
| Ana sayfa: "kiracı izolasyonu veritabanı düzeyinde (RLS)" | **DESTEKLENEN** | Quality 19 RLS politika dosyası; Labs/Exams `014_rls_public_tablolar.py`; IPOS RLS göçleri + izolasyon testi; KursOS RLS göçleri. Dördünde de gerçek. |
| TestRoster: "Community (ücretsiz): 1 uygulama, 14 tester, 14 günlük kampanya" | **DESTEKLENEN + KAPILI** | `packages/contracts/src/plans.ts: FREE_PLAN_LIMITS` birebir aynı; ayrıca `check-plan-matrix-drift.mjs` sunucudaki `plan_features` ile karşılaştırıp sapmada yayını kesiyor. Sitedeki en iyi korunan sayı bu. |
| TestRoster: "Pro $9,99 / Studio $24,99, 3 ve 10 uygulama, ekip koltuğu" | **DOĞRULANAMADI** | Yerelde `supabase/migrations` boş (şema uzakta); ücretli plan limitleri ve fiyatlar koddan doğrulanamıyor. Ayrıca `FAZ-DURUM` Faz 29/39: mağaza satın alma katmanı **bağlı değil**. |
| TestRoster: "Uygulama henüz Play'de değil" | **DESTEKLENEN / dürüst** | Faz 35–36 kısmi; mağaza görselleri üretilmemiş. Sayfa bunu açıkça yazıyor — iyi. |
| IPOS: "Yapay zekâ klinik karar vermez; tanı koymaz" | **DESTEKLENEN / iyi** | Doğru sınır çiziliyor. |
| IPOS: WhatsApp için kliniğin kendi Meta hesabı gerekir | **DESTEKLENEN** | Doğru koşul, sayfada duruyor. |
| Quality: "akreditasyon/denetim/belgelendirme yetkisi taşımaz" | **DESTEKLENEN / iyi** | Gerekli yasal sınır. |
| ChemBioCalc sayfası | **EKSİK** | Lab köprüsü (`app/lab/`: tara/rezervasyon/stok/yoklama/onaylar/sonuç + `lib/unvportal.ts`) hiç anlatılmıyor. |

---

## 4. EKSİK — doğru olup sitede olmayanlar (öncelik sırasıyla)

1. **Quality'nin gerçek kapsamı.** Site 4 kelime; üründe 157 sayfa, 50+ modül: CAPA,
   risk, mevzuat izleme (değişiklik/etki analizi), iç denetim, yönetimin gözden
   geçirmesi, gösterge takibi, OCR, veri odası, SSO, SFTP/DB bağlayıcıları, yetkinlik
   ve vekâlet, mobil uygulama.
2. **Quality'nin raporlama motoru.** `openapi.ts`: *"Deterministik raporlama motoru —
   değişmez snapshot'tan üretim (aynı snapshot → aynı çıktı), SQL/domain'den
   izlenebilir gerçekler (**YZ YOK**), iddia-kanıt doğrulama (**kanıtsız iddia
   UNSUPPORTED**)."* Herkesin "yapay zekâ" dediği yerde "yapay zekâ kullanmıyoruz,
   aynı veriden aynı raporu üretiyoruz" demek ayırt edici bir konum.
3. **ChemBioCalc ↔ Labs köprüsü.** "Aynı ekosistem" iddiasının tek somut kanıtı.
4. **IPOS'ta dikte ve çeviri**, hasta portalı, kiracıya özel alan adı, teklif üretimi.
5. **TestRoster'da Production Readiness Score**, dropout riski, otomatik yerine tester.
6. **Exams'te Excel'den toplu ders/gözetmen aktarımı** ve **madde analizi**.
7. **KursOS'ta WhatsApp kanalı**, öğrenci listesi içe aktarma, dört rollü tek mobil
   uygulama, demo girişi.

---

## 5. Sıradaki iş

1. ~~"Aynı veritabanı" cümlelerini 11 sayfada düzelt (TR+EN birlikte).~~ **YAPILDI**
   (2026-11-08). 12 dosyada 32 cümle düzeltildi: Labs↔Exams için "aynı veritabanı"
   korundu, Quality için "kendi veritabanında çalışır, bu kayıtlardan yalnız okur"
   oldu. `unvportal/index.html` ve EN karşılığındaki bölüm başlığı "Tek kaydın pratik
   karşılığı" / "What a single record means in practice" olarak değişti; her ikisine
   de "Quality kaldırılsa Labs ve Exams aynı şekilde çalışmayı sürdürür" paragrafı
   eklendi. Ana sayfa hero'sundaki "beş platform tek veritabanı üzerinde" iddiası
   (beş ayrı ürün için büsbütün yanlıştı) kaldırıldı; yan panel altlığı "Platformlar
   ayrı ayrı lisanslanır · Türkçe ve İngilizce arayüz" oldu.
2. ~~Labs'teki iki ifadeyi netleştir.~~ **YAPILDI** (2026-11-08). Hatırlatma artık
   "bir gün önce gider; kurulumda zamanlanan görevle otomatik, gerekirse yönetim
   ekranından elle" diyor. Excel içe aktarma iddiası **daraltılmadı, genişletildi** —
   denetimin ilk turu yanılmıştı, özellik gerçek ve self-servis.
3. ~~Quality sayfasını gerçek kapsamıyla yeniden yaz.~~ **YAPILDI** (2026-11-08).
   Sayfa 8 bölümden 14 bölüme çıktı; TR+EN birlikte. Eklenen başlıklar — her biri
   ekran + uç + controller olarak tek tek doğrulandı:
   · **DÖF** (`capa/` 4 ekran, `/capa/overdue`, `/capa/recurrence`, `/capa/{id}/closure-gate`)
   · **Risk ve fırsat** (`risks/` 4 ekran, `/risks/heat-map`, `/risks/{id}/gate`)
   · **İç denetim** (`internal-audit/` 5 ekran, `plans/{id}/external-package`)
   · **Yönetimin gözden geçirmesi**, **gösterge izleme** (`/indicators/{id}/trend`)
   · **Mevzuat yükümlülükleri ve etki analizi** (`compliance/` 8 ekran;
     `regulatory-changes/{id}/impact-preview`). Çift onay kuralı da yazıldı:
     kabul eden, değişikliği girenden farklı VE etkilenen kayıtların sahibi olmak
     zorunda (`regulatory-change.controller.ts` başlığı).
   · **Standart sürüm karşılaştırma / madde soy ağacı / crosswalk + boşluk analizi**
     (`standards-intelligence/`, `/accreditation/crosswalks`, `/gap-analysis`)
   · **Tutanaktan veri çıkarma** (`extraction.controller.ts`: güven düzeyi,
     sayfa konumu, düşük güvende insan seçimi, içe aktarım ayrı yetki)
   · **Deterministik rapor motoru** — kanıtsız iddia UNSUPPORTED, rapor doğrulamadan
     geçmez; YZ gerçeği üretmez, bulguyu cümleye çevirir ve insan onayı olmadan
     yayımlanamaz (`report/` + `extraction/.../ai-report.controller.ts`)
   · **Veri odası** — dış değerlendirici için AYRI guard: davet → e-posta OTP →
     süreli token; yalnız açılan belgeler; her görüntüleme audit
     (`dataroom/interfaces/http-external/`)
   · **Mobil** (`apps/quality-mobile`, Flutter) — saha denetimi, belge tarama,
     çevrimdışı kuyruk, "gönderildi" ile "sırada"nın ayrı gösterilmesi
   · **SSO / yetkinlik / vekâlet / bağlayıcılar** (`federation/`, `competency/`,
     `delegations/`, `self-service-integration/`)
   Süreç yönetimi de tek cümleden genişletildi (görsel modelleme, sürümleme,
   işletim örnekleri, performans panosu, gözden geçirme kuyruğu/kampanyası).
   Sayfa uzadığı için (14 h2) başa sayfa-içi gezinme eklendi; `:target`
   scroll-margin zaten site.css'te olduğu için yapışkan başlık hedefi örtmüyor
   (ölçüldü: başlık 73px, hedef 112px). Diğer 6 sayfadaki Quality özeti de
   güncellendi.
   **Akreditasyon kurumu adı (YÖKAK vb.) hiçbir yere yazılmadı** — kodda yok.
   **Hâlâ açık:** 157 sayfanın kaçının müşteriye açık olduğu ve Quality'nin
   UNVPortal markası altında mı yoksa ayrı `unvplatform` ürünü olarak mı
   satıldığı. Sayfa mevcut "UNVPortal Quality" adlandırmasını korudu.
4. ~~ChemBioCalc ↔ Labs köprüsünü iki sayfaya da ekle.~~ **YAPILDI** (2026-11-08).
   Labs sayfasına (TR+EN) "Cihaz başında telefonla" / "At the bench, on a phone"
   h3'ü, ChemBioCalc sayfasına çift dilli "Kurumsal laboratuvar modülü" bölümü.
   Doğrulanan zincir: `chemcalc-pro/app/lab/` altı ekran (tara, rezervasyon, stok,
   yoklama, onaylar, sonuç) → `lib/unvportal.ts` + `constants/unvportal.ts`
   (`api.unvportal.com/api/v2`) → `unvportal/backend/.../entegrasyon.py`
   `POST /entegrasyon/chembiocalc/baglan`. Yani köprü ESKİ `unvportal` FastAPI
   deposuna bağlanıyor, `unvplatform`a değil.
   Metne giren güvenlik koşulları koddan: kullanıcı UNVPortal'da kayıtlı olmalı
   VE hesabında `chembiocalc` platformu açık olmalı — *"implicit admin bypass
   YOK"*; verilen token kısa ömürlü (2 saat, web oturumu 8 saat); her başarılı
   köprü denetim izine yazılıyor; ekran görünürlüğünü rol yetenekleri belirliyor.
   Ürün gerçeği dosyasının uyarısına uyuldu: köprünün yalnız UNVPortal kurulu
   kurumda çalıştığı her iki metinde de açıkça koşullandırıldı, bağımsız
   kullanıcıya "laboratuvarını yönet" denmedi.
   **Not:** `chembiocalc.com` ayrı depodadır (`chemcalc-pro/apps/web/public`);
   oradaki siteye bu bölüm eklenmedi.

   **Yan bulgu — site genelinde bir stil kusuru düzeltildi.** Bölüm içi h3'lerin
   accent çizgisi `section[aria-labelledby="h-neyapar"]` seçicisine sabitlenmişti.
   EN sayfalarında aynı bölümün id'si `h-does` olduğu için **stil İngilizce
   sayfaların hiçbirinde çalışmıyordu**: ölçüldü, TR Labs h3 padding 18px + 2px
   çizgi, EN Labs 0px + çizgi yok. Aynı sayfa iki dilde farklı görünüyordu.
   `iletisim`, `en/contact`, `en/medical-tourism`, `en/school-management`,
   `en/unvportal/exams`, her iki `unvportal/index` de stilsiz kalıyordu.
   Seçici id'den bağımsız hale getirildi (`section[aria-labelledby] > h3`) ve
   `+ p` → `~ p` yapıldı: önceki hâli yalnız h3'ün İLK paragrafını hizalıyordu,
   iki paragraflı bir h3'te ikincisi hizadan kaçıyordu. 84 sayfanın stil damgası
   yenilendi; 19 sayfa × 2 genişlik taşma/yatay kaydırma taraması temiz.
5. ~~Uygulama içi Labs kullanım kılavuzu ve TestRoster README'si.~~ **YAPILDI**
   (2026-11-08). İkisi de bu deponun dışında, kendi dallarında commit edildi.

   **`unvportal/unvportal` → `duzeltme/kilavuz-iddia-denetimi`** (`9a94a0a6`).
   Kılavuzda denetimin işaretlediği bir değil **üç** bayat iddia çıktı:
   · "Cihaz Envanteri: … kalibrasyon tarihleri" — `CihazEnvanteri` modelinde
     kalibrasyon alanı yok (`models_v2.py:735`); gerçek alanlarla değiştirildi.
   · "Sistemde dört farklı kullanıcı rolü bulunur" — `KullaniciRol` enum'unda
     **altı** rol var (`models_v2.py:25`); `abd_admin` ve `danisman` hiç
     anlatılmıyordu, oysa danışmanın arkasında transkript okuma, müfredat/ön
     koşul analizi ve program çakışma kontrolü olan ayrı bir modül var.
   · "Teknisyen: Sadece ders listesi ve deney yönetimi sayfasına erişir" —
     yetki haritası bunun **tersini** söylüyor: `deps.py:72` teknisyene
     {stok, rezervasyon} veriyor, akademik işlemleri vermiyor.

   **`testroster` → `duzeltme/readme-durum`** (`ec5471d`). README'nin üst
   tablosu "Faz 1 bitti → sıradaki Faz 2" ve "Uygulamalar henüz iskelet"
   diyordu; `docs/FAZ-DURUM.md` sayıldığında **40 fazın tamamı işlenmiş:
   26 bitti, 14 kısmi, 0 bekleyen**. Aşama satırı gerçek sayılarla değişti,
   iskelet cümlesi yerine uygulamaların çalışır olduğu ama **Play'de yayında
   olmadığı** (Faz 35–36 kısmi) yazıldı. Paket tablosuna da uyarı notu kondu:
   tablo satılacak paketleri tarif ediyor, bugünkü çalışır durumu değil —
   satın alma katmanı bağlı değil (29/39), TestProof ağ gönderimi yok (22),
   AI model çağrısı yok (24).

---

**Denetimin beş maddesi de kapandı.** Açık kalanlar madde 4'teki ikinci
öncelik listesinde (IPOS dikte/çeviri, TestRoster readiness score, Exams
madde analizi, KursOS WhatsApp) ve yalnız Ümit'in yanıtlayabileceği sorularda
(hangi UNVPortal kuşağı satılıyor, Quality ayrı marka mı, kurum sayıları).
