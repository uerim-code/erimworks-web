# UNVPortal Labs — ürün gerçeği

**Kaynak:** `~/projects/unvportal/unvportal` (backend FastAPI + `lab-frontend` React).
Son kod değişikliği: backend 2026-10-07, lab-frontend 2026-10-06.
**Tarama tarihi:** 2026-11-06. Bu dosya koddan çıkarıldı; pazarlama metni yazılırken
iddianın dayanağı burada aranır.

## Ne olduğu

Üniversite laboratuvarının günlük işletmesini yürüten tarayıcı tabanlı sistem.
Tek backend (`backend/app`) üzerinde laboratuvar, sınav, yoklama ve danışmanlık
arayüzleri ayrı React uygulamaları olarak çalışıyor.

## Doğrulanmış özellikler

| Özellik | Kanıt | Ölçü |
|---|---|---|
| Stok yönetimi: cihaz, cam/sarf, kimyasal | `api/routes/stok.py` | 41 uç |
| Sarf eksiltme ve hareket defteri | `stok.py`: `/stok/cam-sarf/{id}/eksilt`, `/hareketler` | — |
| Cihaz rezervasyonu (tarih + saat aralığı / tam gün) | `models_v2.py: CihazRezervasyon`, `api/routes/rezervasyon.py` | 20 uç |
| Cihaz QR etiketi | `models_v2.py: CihazEnvanteri.qr_token` (benzersiz, dizinli) | — |
| Yoklama (uygulama) | `api/routes/attendance.py` | 7 uç |
| Teorik ders yoklaması | `api/routes/teorik_yoklama.py` | 10 uç |
| Akademik yapı: fakülte/program/dönem/ders | `api/routes/academic.py` | 28 uç |
| Öğrenci kayıtları ve transkript | `api/routes/students.py`, `pages/TranskriptPage.jsx` | 10 uç |
| Danışmanlık modülü | `api/routes/danisman.py` | 40 uç |
| Değerlendirme + AI puan önerisi kalibrasyonu | `api/routes/evaluation.py` | 15 uç |
| KVKK uçları | `api/routes/kvkk.py` | 2 uç |

Ekranlar (`lab-frontend/src/pages`): AnaSayfa, Panel, Dersler, Kullanıcılar, Profil,
Raporlar, Rezervasyon, Sınav, SınavProgram, StokYönetimi, SüperAdmin, Tahta,
TeorikYoklama, Transkript, ÜrünGiriş, Yoklama + `danisman/` ve `ogrenci/` alt portalları.

## İDDİA EDİLMEMESİ GEREKENLER

- **Cihaz kalibrasyon takibi YOK.** `CihazEnvanteri` modelinin alanları: ad, marka,
  model_no, seri_no, qr_token, konum, açıklama, aktif, oluşturma. **Kalibrasyon tarihi
  alanı yok**, kalibrasyon uyarısı/takvimi yok. Uygulama içindeki kullanım kılavuzu
  (`components/layout/KullaniciKilavuzu.jsx`) "cihaz envanteri: … kalibrasyon tarihleri"
  diyor — bu metin üründe karşılığı olmayan bir vaat, kılavuzda da düzeltilmeli.
- Koddaki tek "kalibrasyon" **AI puan kalibrasyonu**: yapay zekânın önerdiği puanla
  hocanın verdiği final puanın karşılaştırması (`evaluation.py: /ai-kalibrasyon`,
  yalnız admin). Cihazla ilgisi yok; laboratuvar metninde kullanılırsa yanlış anlaşılır.
- LIMS literatüründe standart olan ama burada **bulunmayan** başlıklar: numune zincir
  takibi (chain of custody), akreditasyon dosyası, metot doğrulama, belirsizlik hesabı.

## Açık sorular (kullanıcıya sorulacak)

- Bu nesil (FastAPI + React) hâlâ satılan ürün mü, yoksa `unvplatform` monorepo'suna mı
  taşınıyor? `unvplatform/apps` altında yalnız `quality-web` ve `quality-mobile` var.
- ~~Numune atama iddiasının kod karşılığı~~ **yanıtlandı:** `models_v2.py: Numune`
  modeli gerçek — aktiviteye bağlı, `qr_token`, `gercek_deger`, `tolerans_mutlak`/
  `tolerans_yuzde`, `analit_turu`, durum ve puan dağılımı alanlarıyla. İddia destekli.
