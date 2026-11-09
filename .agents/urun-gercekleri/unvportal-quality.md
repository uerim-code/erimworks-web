# UNVPortal Quality — ürün gerçeği

**Kaynak:** `~/projects/unvportal/unvplatform` (monorepo; `apps/quality-web` Next.js,
`apps/quality-mobile`, `apps/platform-api`, `apps/platform-worker`).
Son commit: **2026-11-05** — portföydeki en aktif geliştirilen B2B ürün.
**Tarama tarihi:** 2026-11-06.

## Ne olduğu

Kalite koordinatörlüklerinin akreditasyon ve iç değerlendirme süreçlerini yürüttüğü
platform. `apps/quality-web/app/(app)` altında **157 sayfa**, 50'den fazla üst düzey modül.

## Doğrulanmış modüller (dizin adlarıyla)

**Kalite döngüsü:** pdca, processes, criteria (+ katalog), standards,
standards-intelligence, indicators, quality-data, quality-calendar, management-reviews,
internal-audit, reports

**Uygunsuzluk ve risk:** capa (+ overdue, recurrence), risks, actions, monitoring

**Mevzuat/uyum:** compliance (changes, impact, matrix, obligations, readiness, watch),
obligations, governance, decisions (+ tracking)

**Kanıt ve belge:** evidence, documents, dataroom, person-documents, ocr

**İnsan ve yetki:** organization, positions, roles, competency, delegations, provisioning,
sso, hesap-baglama, guvenlik, kisisel-alan, my-work

**Entegrasyon:** connectors (sftp-db, nocode, operasyon, kayıt defteri), integration,
migrations, notifications, search, feedback

Ayrıca mobil uygulama (`apps/quality-mobile`) ve arka plan işçisi (`platform-worker`).
Paketler: authorization-sdk, auth-sdk, workflow-core, design-system, design-tokens,
brand-config, observability, contracts.

## Sitenin en büyük eksiği burada

Site Quality'yi dört kelimeyle anlatıyor: *"Kanıt toplama, komisyon ve karar takibi,
PUKÖ döngüsü, iç değerlendirme raporu."* Ürün bunun en az on katı. Sitede hiç geçmeyen,
satın alma kararını doğrudan etkileyen başlıklar:

- **CAPA** (düzeltici/önleyici faaliyet) — gecikme ve tekrar analiziyle birlikte
- **Risk yönetimi**
- **Mevzuat izleme** (compliance/watch, changes, impact): mevzuat değişince hangi
  süreçlerin etkilendiğini çıkarma — bu tek başına bir ürün iddiası
- **İç denetim** modülü
- **Yönetimin gözden geçirmesi** (management-reviews)
- **Gösterge/KPI izleme** (indicators, monitoring)
- **OCR ile belge okuma**
- **Veri odası** (dataroom) — denetçiye kontrollü erişim
- **SSO** ve yetki kataloğu tabanlı yetkilendirme (`authorization-sdk`)
- **Bağlayıcılar**: SFTP/veritabanı aktarımı ve kodsuz entegrasyon
- **Yetkinlik ve vekâlet** yönetimi (competency, delegations)
- **Mobil uygulama**

## İDDİA EDİLMEMESİ GEREKENLER

- Modül dizininin varlığı "ekranı tamamlanmış" demek değil. Metne girecek her başlık
  önce `app/(app)/<modül>/page.tsx` içinde gerçek bir ekran mı diye tek tek bakılmalı
  (bu depoda daha önce "servis var, çağıran ekran yok" vakaları yaşandı).
- Akreditasyon kurumu adı (YÖKAK vb.) kodda doğrulanmadan yazılmamalı.

## Açık sorular

- Quality, UNVPortal markası altında mı satılıyor yoksa `unvplatform` ayrı bir ürün mü?
  Depo adı ve uygulama adları (`platform-api`) ayrı bir marka ima ediyor.
- 157 sayfanın kaçı müşteriye açık, kaçı iç araç?
