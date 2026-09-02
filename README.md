# erimworks-web

erimworks.com için statik site (şimdilik placeholder) + AdMob `app-ads.txt`.

## app-ads.txt
Tüm uygulamalar tek AdMob hesabı (pub-4453331627814444) altında → tek yetkili satıcı satırı.
Mediation eklendikçe her ağ için ek satır girilecek.

## CSP

`_headers` içindeki `Content-Security-Policy` satırı ÜRETİLİR, elle yazılmaz:
politika sayfalardaki satır içi betikleri sha256 ile adlandırıyor.

```
python3 tools/csp.py           # _headers'ı güncelle
python3 tools/csp.py --check   # bayatsa 1 ile çık
```

**Bir satır içi betiği değiştirdikten sonra bunu çalıştır.** Çalıştırılmazsa
hash tutmaz, tarayıcı betiği sessizce bloklar ve hiçbir hata görünmez. Bu
sitede en pahalı kayıp gizlilik/destek sayfalarındaki dil seçicidir — o
sayfalar mağaza uyum yüzeyi.
