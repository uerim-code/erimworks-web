# International Patient OS — ürün gerçeği

**Kaynak:** `~/projects/international-patient-os` (pnpm monorepo: `apps/api` Hono,
`apps/web` Next.js, `apps/mobile` Expo, `apps/worker`).
Son commit: 2026-10-28. **Tarama tarihi:** 2026-11-06.
Canlıda: Hetzner + Coolify; prod App Store sürümü 1.0.0 review sürecinden geçti.

## Ne olduğu

README'nin kendi tanımı: *"Hastanın ilk mesajından teşvik dosyasının kapanışına kadar
tüm süreç tek vaka kaydı üzerinden yönetilir."* Çok kiracılı SaaS; tek klinik için
sabitlenmiş yapı yok.

**Ölçü:** web'de 101 sayfa, API'de 55 rota modülü.

## Doğrulanmış modüller

**Hasta yolculuğu:** lead (+ analiz), intake, hasta kaydı, vaka, teklif (quotes),
hazırlık (readiness), cerrahi planlama (surgery/ameliyat), takip (followup),
komplikasyon, inceleme (review)

**Seyahat ve operasyon:** uçuş (flights), transfer, otel, sürüş, operasyon, görevler,
takvim (+ dışa açık takvim akışı: `calendar-feed.ts`)

**Finans:** vaka finansı, masraf (expenses), ödeme (payments), fatura (invoices),
döviz kuru (fx + `/finans/kurlar`), dışarı aktarma

**Devlet teşviki:** `incentives.ts`, `incentive-operations.ts`, `/tesvik` — teşvik
dosyası üretimi ve operasyonu

**İletişim:** gelen kutusu (tek kutu + ekipler), mesajlaşma, bildirimler ve tercihleri,
çeviri (translation), dikte (dictation, transkript ekranı), AI geçidi (`ai-gateway.ts`)

**Kurumsal:** personel, roller, yetki devri (delegations), iş ortakları (partners),
organizasyonlar, kalite, uyum (compliance), güvenlik (safety), platform/merkez yönetimi,
raporlama, klinik sağlığı

**Hasta portalı:** `/portal` (belgeler, doğrulama) — hasta tarafı

**Altyapı:** kiracıya özel alan adı (`tenant-domains.ts`), gerçek zamanlı (`realtime.ts`),
iş akışı motoru (`workflow.ts`), mobil uç (`mobile.ts`), medya, belge yönetimi

## Sitede eksik anlatılan

Site şu an beş şey sayıyor: *"Tek gelen kutusu, vaka kaydı, cerrahi ve seyahat planı,
vaka finansı, teşvik dosyası."* Doğru ama dar. Sitede hiç geçmeyenler:

- **Dikte ve çeviri** — yurt dışından hasta kabul eden klinikte en çok zaman yiyen iki iş
- **Hasta portalı** ve belge doğrulama
- **Kiracıya özel alan adı** (klinik kendi alan adıyla yayınlar, köken gizli)
- **Teklif (quote) üretimi** ve döviz kuru yönetimi
- **Komplikasyon ve klinik sağlığı izleme**
- **İş ortağı/aracı yönetimi**
- **Mobil uygulama** (saha ekibi için; hastaya yönelik değil)
- **Dışa açık takvim akışı** (Google/Outlook takvimine abonelik)

## İDDİA EDİLMEMESİ GEREKENLER

- **Fatura kesme entegratöre bağlı değil**: e-arşiv altyapısı canlı ama fatura kesme
  entegratör bağlanana kadar DRAFT durumda. "Fatura kesiyor" denmemeli.
- **Hastaya mobil uygulama yok.** Hasta kanalı WhatsApp; mobil uygulamalar saha ekibi için.
- **Teşvik oranı/mevzuatı metne yazılmamalı**: güncel Cumhurbaşkanı Kararı 10962, oran
  %60'tan %50'ye indi. Mevzuat sayısı veya oran siteye yazılacaksa o gün doğrulanmalı.
  KDV/vergi istisnası hibe (grant) değildir; para konusu mali müşavire aittir.
- **Konuşma özeti** özelliği sağlayıcı yapılandırılana kadar "unavailable" dönüyor.
- Outlook takvim entegrasyonu uykuda; yalnız Google canlı ve "Testing" modunda
  (7 günlük token kısıtı).

## Açık sorular

- Bugün kaç klinik kullanıyor? Site "yayındaki platform" diyor, referans sayısı yok.
- Hangi modüller müşteride açık, hangileri bayrak arkasında?
