# UNVPortal Exams — ürün gerçeği

**Kaynak:** `~/projects/unvportal/unvportal/backend` (`api/routes/sinav_otomasyon.py`,
`sinav_program.py`) + `sinav-frontend`; ayrıca ayrı depo `~/projects/unvportal/unvportal-sinav-backend`
ve `unvportal-sinav-frontend`. Son kod değişikliği: 2026-10-07.
**Tarama tarihi:** 2026-11-06.

## Ne olduğu

İki ayrı iş birlikte satılıyor: **sınav otomasyonu** (soru havuzundan sınav üretme,
optik okuma, analiz) ve **sınav programı** (dönem, derslik, gözetmen çizelgesi).

## Doğrulanmış özellikler

### Sınav otomasyonu (`sinav_otomasyon.py`, 37 uç)
- Akademik ağaç: fakülte → program → dönem → ders → konu → soru
- Soru bankası: soru ekleme/güncelleme/silme (`/sorular`, `/sorular/{id}`)
- Sınav oluşturma (`/sinavlar`)
- **Optik form yükleme ve okuma** (`/optik-yukle/{sinav_id}`)
- Sınav analizi (`/analiz/{id}/sinav`) ve **madde analizi** (`/analiz/{id}/madde`)
- İstatistik ucu (`/istatistik`)

### Sınav programı (`sinav_program.py`, 42 uç)
- Dönem yönetimi, derslik tanımları
- Ders tanımları; **toplu ekleme** ve **Excel'den içe aktarma** (`/dersler/toplu`, `/dersler/excel`)
- **Gözetmen listesi Excel'den** (`/gozetmenler/excel`)
- İndirilebilir şablonlar (`/sablon/dersler`)

Ekranlar (`sinav-frontend/src/pages`): Panel, Dersler, Sınavlar, SoruBankası,
Kazanımlar, Analizler.

## Sitede eksik anlatılan

- **Excel ile toplu veri girişi** (ders listesi, gözetmen listesi) sitede hiç geçmiyor;
  oysa kurumsal satın almada en çok sorulan şey "mevcut listemizi nasıl taşırız".
- **Madde analizi** (soru bazında ayırt edicilik/güçlük) ayrı bir değer; site yalnız
  "program çıktısı ölçümü" diyor.
- **Derslik ve gözetmen çizelgesi** apayrı bir iş; site bunu "sınav yönetimi" içinde eritmiş.

## İDDİA EDİLMEMESİ GEREKENLER

- Kopya analizi / benzerlik tespiti kodda yok.
- Çevrimiçi (online) sınav uygulaması yok; akış optik forma dayalı.
- Soru havuzunda madde bankası istatistiği dışında psikometrik model (IRT) yok.

## Açık sorular

- `unvportal-sinav-backend` ayrı deposu ile ana backend'deki `sinav_*` modülleri
  arasındaki ilişki ne? Hangisi müşteride çalışıyor?
