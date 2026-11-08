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
| "Randevu öncesi hatırlatma otomatik gider" | **KISMEN** | Uçlar var (`/hatirlatma`, `/admin/hatirlatma-gonder`, **`/hatirlatma-cron`**) ve mail servisi bağlı. "Otomatik" olması cron'un kurulumda zamanlanmasına bağlı — ürün özelliği değil kurulum adımı. Metin "hatırlatma gönderilir" demeli ya da kurulum notu düşmeli. |
| "Dönem sonunda cihaz başına kullanım raporu" | **DESTEKLENEN** | `/admin/rapor`, `/admin/rezervasyon/{id}/kullanim` |
| "Kritik seviyenin altına düşen malzeme listelenir" | **DESTEKLENEN** | `CamSarf.kritik_adet`, `Kimyasal.kritik_miktar` |
| "Tüketim geçmişi satın alma planı için dışa aktarılır" | **DESTEKLENEN** | `stok.py` → `satin_alma_listesi.xlsx` |
| "Lot ve son kullanma tarihi olan malzemelerde süresi geçenler ayrılır" | **DESTEKLENEN (dar)** | `KimyasalKap`: `lot_no`, `son_kullanma_tarihi`, `acilis_tarihi`. **Yalnız kimyasal kaplarında** — cam/sarf tarafında lot/SKT alanı yok. Cümle "olan malzemelerde" dediği için doğru, ama okuyan bunu sarf için de sanabilir. |
| SSS: "Elektronik tablo halindeki cihaz, sarf ve laboratuvar listeleri kurulum sırasında içe aktarılıyor" | **DOĞRULANAMADI** | `stok.py` içinde excel/csv **içe aktarma ucu yok** (yalnız dışa aktarma var). Bu bir *hizmet* vaadi ise ("kurulum sırasında biz aktarıyoruz") doğru olabilir; ürün özelliği gibi okunuyor. Netleştirilmeli. |
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
2. Labs'teki iki ifadeyi netleştir: hatırlatmanın "otomatik"liği, Excel içe aktarmanın
   ürün mü hizmet mi olduğu.
3. Quality sayfasını gerçek kapsamıyla yeniden yaz — en büyük kazanç orada.
4. ChemBioCalc ↔ Labs köprüsünü iki sayfaya da ekle.
5. Uygulama içi Labs kullanım kılavuzundaki "kalibrasyon tarihleri" ifadesini kaldır
   (üründe karşılığı yok) ve TestRoster README'sinin bayat "iskelet" tablosunu düzelt.
