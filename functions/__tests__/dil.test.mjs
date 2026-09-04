/**
 * Ülke → dil yönlendirmesinin sınaması.
 *
 * ⚠ EN ÖNEMLİ SINAMA "haritadaki her dil DİSKTE VAR MI": haritaya olmayan bir
 * dil yazmak ziyaretçiye 404 verir ve bu sayfalar mağaza uyum yüzeyi.
 *
 * Koşum:  node functions/__tests__/dil.test.mjs
 */
import { readdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { restlaDilYolu } from '../_middleware.js';

const KOK = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
let hata = 0;
const es = (ad, olan, beklenen) => {
  const ok = olan === beklenen;
  if (!ok) hata++;
  console.log(`${ok ? 'ok      ' : '!! HATA '} ${ad}  ->  ${JSON.stringify(olan)}${ok ? '' : `  (beklenen ${JSON.stringify(beklenen)})`}`);
};

console.log('— ülkeye göre —');
es('DE  /restla/privacy', restlaDilYolu('/restla/privacy', 'DE', null), '/restla/de/privacy');
es('BR  /restla/terms',   restlaDilYolu('/restla/terms', 'BR', null), '/restla/pt/terms');
es('JP  /restla/privacy', restlaDilYolu('/restla/privacy', 'JP', null), '/restla/ja/privacy');
es('de  (küçük harf)',    restlaDilYolu('/restla/privacy', 'de', null), '/restla/de/privacy');

console.log('— yönlendirilmemesi gerekenler —');
es('US (eşleşme yok)',    restlaDilYolu('/restla/privacy', 'US', null), null);
es('TR (Türkçe sayfa yok)', restlaDilYolu('/restla/privacy', 'TR', null), null);
es('ülke bilinmiyor',     restlaDilYolu('/restla/privacy', null, null), null);
es('zaten dilli adres',   restlaDilYolu('/restla/de/privacy', 'DE', null), null);
es('başka uygulama',      restlaDilYolu('/qrwise/privacy', 'DE', null), null);
es('ana sayfa',           restlaDilYolu('/', 'DE', null), null);
es('restla kökü',         restlaDilYolu('/restla/', 'DE', null), null);

console.log('— açık istek ülkeyi ezer —');
es('?lang=en (DE ülkede)', restlaDilYolu('/restla/privacy', 'DE', 'en'), null);
es('?lang=fr (DE ülkede)', restlaDilYolu('/restla/privacy', 'DE', 'fr'), '/restla/fr/privacy');
es('?lang=xx (yok)',       restlaDilYolu('/restla/privacy', 'DE', 'xx'), null);

console.log('— haritadaki her dil diskte var mı —');
const dizinler = new Set(readdirSync(resolve(KOK, 'restla'), { withFileTypes: true })
  .filter((d) => d.isDirectory()).map((d) => d.name));
const ulkeler = ['DE','FR','ES','PT','IT','RU','JP','KR','CN','IN','ID','TH','VN','PL','SA','AT','BR','MX','TW','MA'];
for (const u of ulkeler) {
  const yol = restlaDilYolu('/restla/privacy', u, null);
  if (yol === null) { console.log(`!! HATA  ${u} eşleşmedi`); hata++; continue; }
  const dil = yol.split('/')[2];
  const varDizin = dizinler.has(dil);
  const varPrivacy = existsSync(resolve(KOK, 'restla', dil, 'privacy.html'));
  const varTerms = existsSync(resolve(KOK, 'restla', dil, 'terms.html'));
  const ok = varDizin && varPrivacy && varTerms;
  if (!ok) hata++;
  console.log(`${ok ? 'ok      ' : '!! HATA '} ${u} -> ${dil}  (klasör:${varDizin} privacy:${varPrivacy} terms:${varTerms})`);
}

console.log(hata === 0 ? '\nTÜMÜ GEÇTİ' : `\n${hata} HATA`);
process.exit(hata === 0 ? 0 : 1);
