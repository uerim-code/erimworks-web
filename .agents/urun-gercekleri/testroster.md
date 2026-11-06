# TestRoster — ürün gerçeği

**Kaynak:** `~/projects/testroster` (pnpm monorepo: `apps/web` Next.js, `apps/mobile`
Expo/RN, Supabase). Son commit: 2026-10-21. **Tarama tarihi:** 2026-11-06.

## Ne olduğu

Deponun kendi konumlandırması: *"Bu bir 'tester takası' uygulaması **değildir**.
Google Play kapalı test sürecini, gerçek test aktivitesini, geri bildirimi ve
production-readiness hazırlığını yöneten mobil + web platformudur."*

Bu ayrım pazarlamada korunmalı: rakipler tester takası; fark, **ölçülen gerçek test
aktivitesi** ve çıkan **test dosyası**.

## Olgunluk — dikkat

`docs/FAZ-DURUM.md` **40 faz** listeliyor; büyük çoğunluğu "bitti", pgTAP ve vitest
testleriyle. Gerçek WebSocket üretime bağlanıp doğrulanmış (Faz 16).

**Ama `README.md`'nin üst tablosu bayat:** "Faz 1 bitti → sıradaki Faz 2" ve
*"Uygulamalar henüz iskelet; ekranlar Faz 4 ve Faz 5 ile gelir"* diyor. Bu, FAZ-DURUM
ile çelişiyor. Pazarlama metni README'ye değil FAZ-DURUM'a bakmalı; README de
düzeltilmeli (depo kendi olgunluğunu yanlış anlatıyor).

## Doğrulanmış yetenekler

**Kampanya motoru:** 14 günlük durum makinesi, zaman dilimine duyarlı gün hesabı,
denetim kaydı (Faz 8)

**Tester tarafı:** havuz, sunucu tarafı eşleştirme ve yük dengesi (Faz 10), günlük
test görevleri (Faz 11), güvenilirlik/sağlık skoru (Faz 18)

**Ücretli katman:** dropout tespiti ve risk motoru (19), yerine tester motoru (20),
yerine koyma kuyruğu ve süreklilik (21)

**Ölçüm:** oturum başlatıcı ve süre ölçümü (12), senaryo/görev sistemi ve manuel
kapsam (13), ekran/akış kapsam analitiği (23), **Production Readiness Score** (25),
**Production Testing Dossier ve dışa aktarma** (26)

**Geri bildirim:** özel bucket, triyaj koruması, anonim konu (14)

**Altyapı:** offline-first outbox + senkron kuyruğu (15), gerçek zamanlı mobil-web
senkronu row_version/STALE_WRITE ile (16), KVKK/GDPR + consent + veri saklama (31),
yönetici paneli ve plan yönetimi (28), web geliştirici kontrol merkezi (27)

**Planlar:** Community (1 uygulama / 14 tester / 14 gün; dropout bildirimi üretilmiyor,
replacement kapalı) ve ücretli katman (Faz 9).

## İDDİA EDİLMEMESİ GEREKENLER — kısmi kalanlar

Bunlar FAZ-DURUM'da açıkça "kısmi":

- **FCM bağlanmadı** (17) → "anlık bildirim gönderiyoruz" denmemeli
- **TestProof Android SDK**: ağ gönderimi ve cihaz testi yok (22) → SDK'yı çalışır
  gibi anlatma
- **AI Feedback Intelligence**: model çağrısı yok (24) → "yapay zekâ geri bildirimi
  yorumluyor" denmemeli
- **Ödeme/abonelik**: mağaza doğrulaması yok (29), satın alma katmanı bağlı değil (39)
- **Fraud koruması**: cihaz parmak izi yok (30)
- **Observability**: harici APM/alarm kanalı yok (32)
- **Play yayın hazırlığı** (35) ve **mağaza görselleri** (36) kısmi — ekran görüntüleri
  henüz üretilmedi
- Yerel kod tabanında `supabase/migrations` boş görünüyor (şema uzak projede);
  "şu kadar tablo" gibi sayı verilmeden önce uzaktan doğrulanmalı

**Mağaza metni için kapı:** `scripts/check-store-listing.mjs` garanti iddiası,
değerlendirme takası ve kurulum manipülasyonu ifadelerini derlemeyi kırarak engelliyor
(deny-list D2, D4). Site metni de aynı yasakları uygulamalı.

## Sitede eksik anlatılan

Site tek cümle: *"Google Play 14 günlük kapalı test için tester bulma ve ölçülebilir
test dosyası."* Doğru ama şunlar geçmiyor:

- **Production Readiness Score** — sayısal bir çıktı, satışın en somut vaadi
- **Dropout riski ve otomatik yerine tester** — kapalı testin asıl acısı budur
- **Ekran/akış kapsam analitiği**
- **Ücretsiz Community planı** (1 uygulama / 14 tester / 14 gün) — deneme kapısı

## Açık sorular

- Play'de yayında mı, hangi aşamada? `store/play-listing.*.md` hazır ama görseller yok.
- Site TestRoster'ı "uygulama" listesinde mi, "platform" listesinde mi göstermeli?
