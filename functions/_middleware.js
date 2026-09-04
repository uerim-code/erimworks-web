/**
 * www.erimworks.com → erimworks.com (kalıcı 301)
 *
 * NEDEN BURADA, _redirects'te DEĞİL:
 * Cloudflare Pages'in _redirects dosyası domain seviyesi yönlendirmeyi
 * desteklemiyor (dokümanda ❌ işaretli); yalnız YOL eşlemesi yapar, host'a
 * bakamaz. Bu yüzden www→apex ya bir Pages Function ile (bu dosya) ya da
 * panelden Redirect Rule ile kurulur. Depoda kalsın ve sürüm takibine girsin
 * diye Function seçildi — aynı çözüm perimlab.com'da kurulup CANLIDA
 * doğrulandı (www → 301).
 *
 * ÖLÇÜLEN SORUN (2026-08-29): www.erimworks.com ayrı host olarak HTTP 200
 * dönüyordu. Sayfadaki canonical apex'i gösterdiği için Google ikisini
 * birleştiriyor — yani bu bir sıralama kaybı DEĞİL; ama iki host da taranıyor
 * ve tarama bütçesi bölünüyor. 301 daha temiz.
 *
 * PANEL ALTERNATİFİ (bu Function devreye girmezse):
 *   Rules → Redirect Rules → Single Redirect
 *   If:   hostname eşittir  www.erimworks.com
 *   Then: Dynamic → concat("https://erimworks.com", http.request.uri.path)
 *         Status 301, "Preserve query string" açık.
 *
 * KIRMIZI ÇİZGİ: bu sitedeki gizlilik/EULA sayfaları App Store ve Play
 * listelemelerinde kullanılıyor. Yönlendirme YOLU KORUR (yalnız host değişir),
 * dolayısıyla /qrwise/privacy gibi adresler çalışmaya devam eder. Yalnız tam
 * olarak www.erimworks.com yönlendirilir; *.pages.dev önizlemelerine dokunulmaz.
 */
/* ─────────────────────── Restla hukuki sayfaları: dil ─────────────────────── */

/**
 * ***NEDEN BURADA, SITEMAP'TE DEĞİL.***
 *
 * Restla'nın gizlilik ve kullanım koşulları 15 dilde AYRI SAYFA olarak duruyor
 * (`/restla/de/privacy` gibi); kök adresler (`/restla/privacy`) İngilizce.
 * Alternatif, 30 adresi sitemap'e yazıp karşılıklı hreflang kurmaktı; ürün
 * kararı bunun yerine ziyaretçinin GİRDİĞİ ÜLKEYE göre doğru dili göstermek
 * oldu (Ümit, 2026-09-03).
 *
 * Ülke bilgisi Cloudflare'den geliyor (`request.cf.country`, yedeği
 * `CF-IPCountry` başlığı). Bu değeri KENARDA CLOUDFLARE yazar; istemci
 * uyduramaz. Yani dil seçimi güvenilir bir sinyale dayanıyor.
 *
 * ⚠ ***YÖNLENDİRME KALICI OLAMAZ (301 DEĞİL, 302).*** Yanıt ziyaretçiye göre
 * değişiyor; 301 tarayıcıda sonsuza kadar önbelleklenir ve kişiyi gördüğü ilk
 * dile KİLİTLER — sonra yurt dışına çıkan ya da VPN kapatan kullanıcı yanlış
 * dilde kalır.
 *
 * ⚠ ***İNGİLİZCEYE DÖNÜŞ YOLU BIRAKILDI.*** İngilizce ayrı bir klasörde değil,
 * kök adresin kendisinde. Ülke eşleşmesi olan bir ziyaretçi kök adrese her
 * girdiğinde yönlendirilseydi İngilizceye ULAŞAMAZDI. Bu yüzden `?lang=`
 * açıkça verildiğinde ülke algılaması DEVREDE DEĞİL: `?lang=en` İngilizce'de
 * bırakır, `?lang=de` Almanca'ya götürür. Destek taleplerinde ve sınamada da
 * tek tutamak bu.
 *
 * ⚠ ***KIRMIZI ÇİZGİ KORUNUYOR:*** bu adresler App Store ve Play
 * listelemelerinde kullanılıyor. Yönlendirme yalnız DİL ekler, sayfayı
 * kaldırmaz; her dil sayfası kendi adresinden 200 dönmeye devam eder ve
 * eşleşmeyen her ülke İngilizce kök sayfada kalır.
 */

// Diskteki `restla/<kod>/` klasörleriyle BİREBİR aynı olmalı. Buraya olmayan
// bir dil yazılırsa ziyaretçi 404 görür — bu yüzden liste elle kısa tutuldu ve
// `tools/csp.py` gibi bir üreticiye bağlanmadı; değişimi nadir.
const RESTLA_DILLERI = new Set([
  'ar', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja', 'ko', 'pl', 'pt', 'ru', 'th', 'vi', 'zh',
]);

/**
 * Ülke → dil. Listede OLMAYAN her ülke İngilizce kök sayfada kalır; bu bilinçli
 * bir varsayılan, eksiklik değil (Türkiye dahil — Restla'nın Türkçe sayfası yok).
 */
const ULKE_DILI = {
  // Almanca
  DE: 'de', AT: 'de', CH: 'de', LI: 'de',
  // Fransızca
  FR: 'fr', BE: 'fr', LU: 'fr', MC: 'fr', SN: 'fr', CI: 'fr', ML: 'fr', BF: 'fr',
  NE: 'fr', TG: 'fr', BJ: 'fr', GA: 'fr', CD: 'fr', CM: 'fr',
  // İspanyolca
  ES: 'es', MX: 'es', AR: 'es', CO: 'es', CL: 'es', PE: 'es', VE: 'es', EC: 'es',
  GT: 'es', CU: 'es', BO: 'es', DO: 'es', HN: 'es', PY: 'es', SV: 'es', NI: 'es',
  CR: 'es', PA: 'es', UY: 'es', GQ: 'es',
  // Portekizce
  PT: 'pt', BR: 'pt', AO: 'pt', MZ: 'pt',
  // İtalyanca
  IT: 'it', SM: 'it', VA: 'it',
  // Rusça
  RU: 'ru', BY: 'ru', KZ: 'ru', KG: 'ru',
  // Doğu Asya
  JP: 'ja', KR: 'ko', CN: 'zh', TW: 'zh', HK: 'zh', MO: 'zh', SG: 'zh',
  // Güney/Güneydoğu Asya
  IN: 'hi', ID: 'id', TH: 'th', VN: 'vi',
  // Lehçe
  PL: 'pl',
  // Arapça
  SA: 'ar', AE: 'ar', EG: 'ar', QA: 'ar', KW: 'ar', BH: 'ar', OM: 'ar', JO: 'ar',
  LB: 'ar', IQ: 'ar', SY: 'ar', YE: 'ar', LY: 'ar', DZ: 'ar', MA: 'ar', TN: 'ar',
  SD: 'ar', PS: 'ar', MR: 'ar',
};

/** Kök Restla hukuki adresleri: yalnız bunlar yönlendirilir (dilli adresler DEĞİL). */
const RESTLA_KOK = /^\/restla\/(privacy|terms)$/;

/**
 * Yönlendirilecek yolu döndürür, yoksa null. SAF fonksiyon — sınanabilir olsun
 * diye dışa aktarıldı (`functions/__tests__/dil.test.mjs`).
 */
export function restlaDilYolu(pathname, ulke, aciklananDil) {
  const eslesme = RESTLA_KOK.exec(pathname);
  if (eslesme === null) return null;
  const sayfa = eslesme[1];

  // Açık istek her zaman ülkeyi EZER.
  if (typeof aciklananDil === 'string' && aciklananDil !== '') {
    if (aciklananDil === 'en') return null;
    return RESTLA_DILLERI.has(aciklananDil) ? `/restla/${aciklananDil}/${sayfa}` : null;
  }

  const dil = ULKE_DILI[String(ulke ?? '').toUpperCase()];
  if (dil === undefined || !RESTLA_DILLERI.has(dil)) return null;
  return `/restla/${dil}/${sayfa}`;
}

export const onRequest = async (context) => {
  try {
    const url = new URL(context.request.url);
    if (url.hostname === 'www.erimworks.com') {
      url.hostname = 'erimworks.com';
      return Response.redirect(url.toString(), 301);
    }

    // Ülkeye göre dil — yalnız Restla kök hukuki adreslerinde.
    const ulke = context.request.cf?.country ?? context.request.headers.get('CF-IPCountry');
    const hedef = restlaDilYolu(url.pathname, ulke, url.searchParams.get('lang'));
    if (hedef !== null) {
      const yeni = new URL(url.toString());
      yeni.pathname = hedef;
      yeni.searchParams.delete('lang');
      // 302: yanıt ziyaretçiye göre değişir, kalıcı olamaz.
      return new Response(null, {
        status: 302,
        headers: { Location: yeni.toString(), 'Cache-Control': 'no-store' },
      });
    }
  } catch (_) {
    // Yönlendirme kurulamazsa site normal servis edilmeye devam etsin;
    // bu ara katman hiçbir koşulda sayfayı düşürmemeli.
  }
  return context.next();
};
