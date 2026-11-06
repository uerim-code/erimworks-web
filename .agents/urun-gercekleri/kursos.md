# KursOS — ürün gerçeği

**Kaynak:** sunucu `~/projects/merkur-saas` (Next.js `apps/web` + `apps/worker`),
mobil `~/projects/kursos-mobile` (Expo). `~/projects/kursos` arşiv — orada çalışılmaz.
Son commit: sunucu 2026-11-04, mobil 2026-11-04. **Tarama tarihi:** 2026-11-06.

**Ad:** Merkür SaaS'ın ürün adı KursOS. Jenerik satılıyor; her kurulum beyaz etiket.
Tek kod, tek dağıtım: kurum kopyalanmaz, alan adı eklenir.

## Ölçü

Sunucuda 43 sayfa, 48 API ucu. Mobilde dört rol ekranı (koordinatör, öğretmen,
öğrenci, misafir).

## Doğrulanmış modüller — sunucu

**Eğitim işletmesi:** dersler (+ yeni), takvim, öğrenciler (+ içe aktarma),
bekleme listesi, ödevler, duyurular, onaylar

**Ayarlar (kurulum yüzeyi):** alan adları, entegrasyonlar, hatırlatmalar, hizmetler,
kampanyalar, kullanıcılar, mobil, odalar, öğretmenler, organizasyon, paketler,
şablonlar, veliler

**Finans:** tahsilat ve **öğretmen hakedişi** (`finans/hakedis`)

**Kanallar:** WhatsApp (ayrı modül + API ucu), duyurular, hatırlatma şablonları

**Portal:** `/portal` — veli/öğrenci tarafı

**Platform:** `/platform` (kiracı yönetimi), yedek (`/yedek`, `api/yedek`),
raporlar, KVKK ucu, medya, belge, ödev dosyası, geçici parola, webhooks

## Doğrulanmış — mobil (tek mağaza uygulaması)

- Dört ayrı giriş: **Koordinatör**, **Öğretmen**, **Öğrenci**, **Misafir**
- Yoklama düğmeleri (öğretmenin sahada en çok kullandığı iş)
- Sekmeler: dersler, duyurular, ödevler, araçlar, paketler, kurumlar, başvuru
- Kurum seçimi (`kurumlar.tsx`) — tek uygulamadan çok kuruma bağlanma
- **Reklam** (`src/ads`: banner + geçiş reklamı) ve **abonelik** (`src/purchases`)
  altyapısı var: misafir/öğrenci tarafı reklamlı, Pro tarafı abonelikli
- Demo girişi: demo verisi her girişte bugüne tazeleniyor

## Sitede eksik anlatılan

Site: *"Ders programı, paket ve bekleme listesi, veli portalı, tahsilat ve hakediş;
beyaz etiket."* Doğru ama sitede geçmeyen ve satışta işe yarayanlar:

- **WhatsApp kanalı** ve hatırlatma şablonları
- **Öğrenci listesini içe aktarma** (`ogrenciler/ice-aktar`) — taşıma itirazını karşılar
- **Dört rollü tek mobil uygulama** ve kurum seçimi
- **Kendi alan adı** (`ayarlar/alan-adlari`)
- **Kampanya** ve **hizmet/paket** tanımları
- **Yedekleme** ve onay akışı
- **Demo girişi** — denemek isteyene tek düğme

## İDDİA EDİLMEMESİ GEREKENLER

- Mobil uygulama **tek** uygulamadır; "her kuruma özel mağaza uygulaması" denmemeli
  (kurum seçimi uygulama içinde).
- Play'de bugüne kadar **satın alma gerçekleşmemiş**; "binlerce abone" türü sayı yok.
- Yerel `localhost:3000` üretim derlemesidir, bayat kalır; ekran görüntüsü alınacaksa
  önce yeniden derlenir.

## Açık sorular

- Kaç kurum canlıda? Site referans vermiyor.
- "Sanat, müzik ve dil okulları" dışında kullanan kurum tipi var mı?
