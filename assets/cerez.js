/* Çerez rızası ve ölçüm — tek dosya, satır içi betik yok.
 *
 * KARAR: RIZA VERİLMEDEN GOOGLE TAG MANAGER HİÇ YÜKLENMEZ.
 *
 * Google'ın önerdiği yol "Consent Mode v2"dir: GTM her zaman yüklenir, rıza
 * yokken çerez YAZMAZ ama anonim ping gönderir. Burada o yol seçilmedi,
 * çünkü "Reddet"e basan ziyaretçinin tarayıcısından Google'a hiçbir istek
 * gitmemesi savunması kolay tek davranıştır; bazı denetim otoriteleri
 * çerezsiz ping'i de izleme sayıyor. Rıza bilgisi `localStorage`da durur,
 * çerez bile kullanılmaz.
 *
 * Rıza verilince yine de Consent Mode varsayılanları dataLayer'a yazılır:
 * GTM kabul akışında yüklendiğinde doğru durumla başlasın diye. Reklam
 * kişiselleştirmesi ve reklam kullanıcı verisi HER DURUMDA kapalıdır —
 * ziyaretçi "Kabul et" dese bile. Buradan ölçülmek istenen şey hangi ürün
 * sayfasının okunduğu; kişi bazlı reklam profili değil.
 *
 * Bant yalnız karar verilmemişken görünür. Karardan sonra sayfanın altındaki
 * "Çerez tercihi" bağlantısı onu yeniden açar (gizlilik sayfasının gereği:
 * verilen rıza aynı kolaylıkla geri alınabilmeli).
 */
(function () {
  'use strict';

  var GTM = 'GTM-TPV949ZK';
  var ANAHTAR = 'ew-cerez';           // localStorage anahtarı
  var SURUM = 1;                      // metin/kapsam değişirse artır, rıza yenilenir

  var EN = document.documentElement.lang === 'en';
  var M = EN ? {
    metin: 'We use measurement cookies to see which pages are read. They are not set unless you accept, and no advertising profile is built either way.',
    detay: 'Privacy notice',
    kabul: 'Accept',
    ret: 'Decline',
    etiket: 'Cookie notice',
    tercih: 'Cookie preference'
  } : {
    metin: 'Hangi sayfaların okunduğunu görmek için ölçüm çerezi kullanıyoruz. Kabul etmezseniz yerleştirilmez; her iki durumda da reklam profili çıkarılmaz.',
    detay: 'Gizlilik bildirimi',
    kabul: 'Kabul et',
    ret: 'Reddet',
    etiket: 'Çerez bildirimi',
    tercih: 'Çerez tercihi'
  };
  /* EN ziyaretçi TR metnin ortasına düşmesin: gizlilik sayfasının İngilizce özeti. */
  var GIZLILIK = EN ? '/gizlilik/#h-en' : '/gizlilik/#h-cerez';

  function oku() {
    try {
      var ham = window.localStorage.getItem(ANAHTAR);
      if (!ham) return null;
      var v = JSON.parse(ham);
      return v && v.s === SURUM ? v.k : null;   // k: true/false
    } catch (e) { return null; }                // özel pencere / kapalı depolama
  }

  function yaz(kabul) {
    try {
      window.localStorage.setItem(ANAHTAR, JSON.stringify({ s: SURUM, k: kabul, t: Date.now() }));
    } catch (e) { /* yazılamıyorsa karar bu oturumluk geçerli */ }
  }

  /* Rıza geri alınınca ölçüm çerezleri SİLİNİR.
   *
   * ÖLÇÜLDÜ (2026-11-11, canlı): kabul edip sonra reddeden ziyaretçide yeni
   * istek gitmiyordu ama `_ga` ve `_ga_<konteyner>` çerezleri tarayıcıda
   * duruyordu. Rızanın geri alınması, verilmesi kadar etkili olmalı; kalan
   * çerez bir sonraki kabulde aynı kimliği geri getirir.
   *
   * Çerez hangi alan adıyla yazıldıysa o alan adıyla silinir: GA4 çerezi
   * genelde `.erimworks.com` kaydeder, oysa silme denemesi varsayılan olarak
   * tam ana makineye yazar ve hiçbir şey silinmez. Bu yüzden boş alan adı,
   * ana makine ve kök alan adı — üçü birden denenir.
   */
  function olcumCerezleriniSil() {
    var host = location.hostname;
    var alanlar = ['', host, '.' + host];
    var parca = host.split('.');
    if (parca.length > 2) alanlar.push('.' + parca.slice(-2).join('.'));

    document.cookie.split(';').forEach(function (ham) {
      var ad = ham.split('=')[0].trim();
      if (!/^(_ga|_gid|_gat)/.test(ad)) return;
      alanlar.forEach(function (d) {
        document.cookie = ad + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' +
          (d ? '; domain=' + d : '');
      });
    });
  }

  /* Consent Mode varsayılanları — GTM'den ÖNCE dataLayer'a girmeli. */
  function rizaVarsayilani() {
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag('consent', 'default', {
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      analytics_storage: 'denied',
      functionality_storage: 'granted',
      security_storage: 'granted'
    });
    gtag('js', new Date());
  }

  function rizaGuncelle() {
    function gtag() { window.dataLayer.push(arguments); }
    gtag('consent', 'update', { analytics_storage: 'granted' });
  }

  /* Reddetme anında ölçüm sinyalini KAPAT.
   *
   * ÖLÇÜLDÜ (2026-11-13, canlı): kabul edip sonra reddeden ziyaretçide `_ga`
   * siliniyordu ama `_ga_<konteyner>` hayatta kalıyordu. Sebep: rıza geri
   * alınırken sinyal hiç `denied`e çevrilmiyordu, yani sayfadaki GA4 hâlâ
   * ölçüyordu ve oturum çerezini her olayda yeniden yazıyordu — silme ile
   * yazma yarışıyordu. Sinyal önce kapanır, çerezler SONRA silinir.
   */
  function rizaKapat() {
    if (!yuklendi) return;
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    gtag('consent', 'update', { analytics_storage: 'denied' });
  }

  var yuklendi = false;
  function gtmYukle() {
    if (yuklendi || !GTM) return;
    yuklendi = true;
    rizaVarsayilani();
    rizaGuncelle();
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM;
    document.head.appendChild(s);
  }

  function bantKur() {
    var b = document.createElement('div');
    b.className = 'cerez';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', M.etiket);

    var p = document.createElement('p');
    p.className = 'cerez-metin';
    p.appendChild(document.createTextNode(M.metin + ' '));
    var a = document.createElement('a');
    a.href = GIZLILIK;
    a.textContent = M.detay;
    p.appendChild(a);

    var kutu = document.createElement('div');
    kutu.className = 'cerez-dugmeler';
    var ret = document.createElement('button');
    ret.type = 'button';
    ret.className = 'btn btn-sm btn-quiet';
    ret.textContent = M.ret;
    var kabul = document.createElement('button');
    kabul.type = 'button';
    kabul.className = 'btn btn-sm btn-primary';
    kabul.textContent = M.kabul;

    /* "Reddet" önce gelir ve "Kabul et" ile aynı ağırlıktadır: rıza, reddetmek
       kabul etmekten zorsa serbestçe verilmiş sayılmaz. */
    kutu.appendChild(ret);
    kutu.appendChild(kabul);
    b.appendChild(p);
    b.appendChild(kutu);

    function kapat() { b.remove(); }

    /* REDDEDİNCE SAYFAYI YENİLE.
     *
     * GTM bir kez yüklendikten sonra sayfadan KALDIRILAMAZ: kurduğu dinleyiciler
     * yaşamaya devam eder. Sinyali kapatıp `_ga*` çerezlerini silmek yeni çerez
     * yazılmasını ve kişiye bağlanmayı engelliyor, ama etiketin yüklü olduğu bir
     * sayfada reddetme anında ölçüme bir istek daha gidebiliyor (çerezsiz).
     * Rızanın geri alınması, verilmesi kadar etkili olmalı; bir kez yüklenen
     * etiketten kurtulmanın tek yolu sayfayı yenilemek.
     *
     * İki koşul birlikte aranır:
     *   - `yuklendi` — GTM gerçekten bu sayfada yüklendi. Karar verilmemişken
     *     "Reddet" seçene yenileme yapılmaz: orada yüklenmiş bir şey yok ve
     *     sayfayı sebepsiz yenilemek okuyana yerini kaybettirir.
     *   - `oku() === false` — karar depolamaya KALICI yazıldı. Gizli pencerede
     *     localStorage yazamıyoruz; yenileme kararı silip bandı geri getirir,
     *     yani reddeden ziyaretçiye aynı soruyu tekrar sorardı.
     */
    ret.addEventListener('click', function () {
      yaz(false);
      rizaKapat();
      olcumCerezleriniSil();
      if (yuklendi && oku() === false) { location.reload(); return; }
      kapat();
    });
    kabul.addEventListener('click', function () { yaz(true); gtmYukle(); kapat(); });

    document.body.appendChild(b);
    ret.focus();
  }

  function baslat() {
    var karar = oku();
    if (karar === true) { gtmYukle(); return; }
    /* Karar "reddet" ise her açılışta ölçüm çerezleri silinir. Yenileme ve
       sinyal kapatma yarışı kapatıyor, bu satır kapanmayan her ihtimali
       kapatıyor: reddeden ziyaretçinin tarayıcısında ölçüm çerezi KALMAZ. */
    if (karar === false) { olcumCerezleriniSil(); return; }
    bantKur();
  }

  /* Altbilgideki "Çerez tercihi" bağlantısı kararı sıfırlar ve bandı geri getirir. */
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-cerez-ayar]') : null;
    if (!t) return;
    e.preventDefault();
    try { window.localStorage.removeItem(ANAHTAR); } catch (err) { /* yok sayılır */ }
    olcumCerezleriniSil();
    if (!document.querySelector('.cerez')) bantKur();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', baslat);
  } else {
    baslat();
  }
})();
