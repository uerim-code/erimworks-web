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
export const onRequest = async (context) => {
  try {
    const url = new URL(context.request.url);
    if (url.hostname === 'www.erimworks.com') {
      url.hostname = 'erimworks.com';
      return Response.redirect(url.toString(), 301);
    }
  } catch (_) {
    // Yönlendirme kurulamazsa site normal servis edilmeye devam etsin;
    // bu ara katman hiçbir koşulda sayfayı düşürmemeli.
  }
  return context.next();
};
