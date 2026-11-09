# Suİz — Donanım Temin ve Hazırlık Planı

> **Senkronizasyon:** Bu belge Notion ana dokümanıyla senkron tutulur (bkz. [AGENTS.md](../AGENTS.md)). Notion güncel görev durumunun, bu belge yayınlanacak teknik kaydın ana kaynağıdır.
>
> Hazırlayan: donanım ve tesisat sorumlusu · İlk sürüm: 17 Ekim 2026 · Sadeleştirilmiş sürüm: 20 Ekim 2026
> Fiyatlar 20.10.2026'da robotistan.com ve direnc.net ürün sayfalarında görülen KDV dahil liste fiyatlarıdır. Stok durumu aynı gün ürün sayfalarından tek tek kontrol edildi. Sipariş öncesi sepette tekrar bakılmalıdır.

## 1. Kapsam ve varsayımlar

| Konu | Karar |
| :--- | :--- |
| **Hazırlık süresi** | Donanım ve MVP için 9–22 Kasım 2026. Bitki yetiştirme dahil toplam süre 30 Aralık'a kadar; güncel takvim README §11 ve Notion'dadır |
| **Konum** | Adana, balkon |
| **Temin kuralı** | Elektronik kalemlerin tamamı Robotistan'dan alınır. Tek istisna kapasitif toprak nem sensörüdür (Robotistan'da yok, bkz. [Bölüm 3](#3-robotistan-dışı-tek-kalem)) |
| **Bütçe** | 50 USD Robotistan hediye çeki. Çeki aşan kısım ve kargo eşiği ekip tarafından karşılanır |
| **Deneyim** | Ekip ilk kez tesisat ve devre kuruyor. Bu yüzden kritik her kalemden **en az bir yedek** alınır; deneme için breadboard, kalıcı kurulum için pertinaks ve lehim malzemesi listeye eklenmiştir |
| **Sadeleştirme** | İlk plana göre 6 kalem çıkarıldı (bkz. [Bölüm 5](#5-sadeleştirme-ve-gerekçeleri)). Başvurunun çekirdek iddiaları (A/B deneyi, iki derinlikte kapasitif ölçüm, akışla doğrulanan sulama, MCU'da donanımsal emniyet) aynen korunur |

## 2. Robotistan sipariş listesi

Tüm kalemler 20.10.2026'da **stokta**, sipariş **teslim alındı** (Kasım 2026). Fiyatlar KDV dahildir.

### 2.1 Çekirdek elektronik

| # | Ürün (Robotistan adı) | Kullanılan | Alınacak | Birim (TL) | Toplam (TL) | Rolü / not |
| :-: | :--- | :-: | :-: | --: | --: | :--- |
| 1 | [Su Akış Sensörü YF-S401 Debimetre 0.3-6L/Min 3.5mm - Beyaz](https://www.robotistan.com/yfs401-akis-sensoru-3mm) | 2 | **3** | 226,33 | 678,99 | Yatak başına akış ve hacim. Depo hacmi de bundan hesaplanır |
| 2 | [Mini Dalgıç Su Pompası 6V 120 Litre/Saat](https://www.robotistan.com/mini-dalgic-pompa-6v-120-litresaat) | 2 | **4** | 50,09 | 200,36 | 2,5–6 V, 130–220 mA. Giriş 4,7 mm, çıkış 7,5 mm. 5 V ile doğrudan çalışır |
| 3 | [LR7843 MOSFET Sürücü Kartı](https://www.robotistan.com/lr7843-mosfet-kontrol-modulu) | 2 | **3** | 48,89 | 146,67 | Optokuplörlü, 3,3–5 V sinyalle tetiklenir |
| 4 | [Su Seviye Sensörü (91x24 mm) - ZP7510](https://www.robotistan.com/su-seviye-sensoru-91x24-mm-zp7510) | 2 | **3** | 145,45 | 436,35 | Şamandıra: yazılımdan bağımsız düşük seviye kilidi |
| 5 | [DHT22 Dijital Sıcaklık ve Nem Sensörü Modülü](https://www.robotistan.com/dht22-sicaklik-nem-sensoru-modulu) | 1 | **2** | 105,62 | 211,24 | Modül tipi (3,3–5 V). Ortam sıcaklık/nem, VPD ve ET₀ hesabı |
| 6 | [5V 2A DC Adaptör 5.5mm x 2.1mm - 1 Metre Kablo](https://www.robotistan.com/5v-2a-dc-adaptor-55mm-x-21mm-1-metre-kablo) | 1 | **1** | 142,44 | 142,44 | Pompa ve sensör hattı. UNO Q ayrı beslenir (bkz. §6) |
| 7 | [Klemens Girişli DC Barrel Jack](https://www.robotistan.com/klemens-girisli-dc-barrel-jack-dc-barrel-to-wire-jack) | 1 | **2** | 9,66 | 19,32 | Adaptör girişi |
| 8 | [1N5819 Diyot](https://www.robotistan.com/1n5819-diyot) | 2 | **10** | 2,96 | 29,60 | Pompa flyback koruması |
| 9 | [1/4 W 10K Direnç Paketi](https://www.robotistan.com/14w-10k-direnc-paketi-10-adet) | 2 | **20** | 0,24 | 4,80 | Akış darbe hatlarında 5 V → 3,3 V bölücü (üst direnç) |
| 10 | [1/4 W 20K Direnç Paketi](https://www.robotistan.com/14w-20k-direnc-paketi-10-adet) | 2 | **20** | 0,24 | 4,80 | Bölücünün alt direnci |
| | **Çekirdek toplam** | | | | **≈ 1.874,57** | |

### 2.2 Bağlantı ve montaj

| # | Ürün | Alınacak | Birim (TL) | Toplam (TL) | Not |
| :-: | :--- | :-: | --: | --: | :--- |
| 11 | [30 cm 40 Pin Dişi-Erkek Jumper Kablo](https://www.robotistan.com/30cm-40-pin-ayrilabilen-disi-erkek-m-f-jumper-kablo-300-mm) | 1 | 59,75 | 59,75 | Modül → breadboard |
| 12 | [30 cm 40 Pin Erkek-Erkek Jumper Kablo](https://www.robotistan.com/30cm-40-pin-ayrilabilen-erkek-erkek-m-m-jumper-kablo-300-mm) | 1 | 63,98 | 63,98 | Breadboard içi |
| 13 | [30 cm 40 Pin Dişi-Dişi Jumper Kablo](https://www.robotistan.com/30cm-40-pin-ayrilabilen-disi-disi-f-f-jumper-kablo-300-mm) | 1 | 56,73 | 56,73 | Modül → modül |
| 14 | [Orta Boy Breadboard](https://www.robotistan.com/orta-boy-breadboard) | 2 | 36,09 | 72,18 | Lehimsiz deneme; her yatak için bir tane |
| 15 | [10x10 cm Delikli Pertinaks (Bakır) Tek Yüzlü](https://www.robotistan.com/10x10-cm-delikli-pertinaks-tek-yuzlu) | 3 | 42,85 | 128,55 | Kalıcı kurulum (1 ana kart + 2 deneme/yedek) |
| 16 | [KF2EDGR-5.08-2P Geçmeli Klemens](https://www.robotistan.com/kf2edgr-508-2p) | 10 | 7,91 | 79,10 | Güç, pompa, şamandıra bağlantıları (pertinaksa lehimlenir) |
| 17 | [KF2EDGR-5.08-3P Geçmeli Klemens](https://www.robotistan.com/kf2edgr-508-3p) | 10 | 11,29 | 112,90 | Sensör bağlantıları (VCC–GND–sinyal) |
| 18 | [Tek Damar Montaj Kablosu 24AWG 20m - Kırmızı](https://www.robotistan.com/tek-damar-montaj-kablosu-24awg-20m-kirmizi) | 1 | 133,38 | 133,38 | Kalıcı kablolama (+) |
| 19 | [Tek Damar Montaj Kablosu 24AWG 20m - Siyah](https://www.robotistan.com/tek-damar-montaj-kablosu-24awg-20m-siyah) | 1 | 133,38 | 133,38 | Kalıcı kablolama (GND) |
| 20 | [Renkli Makaron Seti - 328 Adet](https://www.robotistan.com/328-adet-renkli-makaron) | 1 | 123,73 | 123,73 | Lehim noktalarının ve sensör kablolarının yalıtımı. *Stok az (4 adet)* |
| 21 | [Küçük Kablo Bağı Paketi - 100 Adet (150 mm)](https://www.robotistan.com/kucuk-kablo-bagi-paketi-100-adet-150mm) | 1 | 55,53 | 55,53 | Kablo düzeni, hortum sabitleme |
| 22 | [8 mm Çift Uçlu Timsah Ağızlı Krokodil Kablo - 10 Adet](https://www.robotistan.com/8-mm-cift-uclu-orta-boy-timsah-agizli-krokodil-kablo-35-27-mm-45-cm-10-adet) | 1 | 77,86 | 77,86 | Pompa ve şamandırayı lehimlemeden denemek için |
| | **Bağlantı ve montaj toplamı** | | | **≈ 1.097,07** | |

### 2.3 Alet (evde yoksa)

| # | Ürün | Alınacak | Birim (TL) | Not |
| :-: | :--- | :-: | --: | :--- |
| 23 | [DT830D Dijital Multimetre](https://www.robotistan.com/dt830d-dijital-multimetre-siyah-1) | 1 | 298,76 | **İlk kez kuran biri için en önemli alet:** gerilim, süreklilik ve bölücü çıkışı (≤ 3,3 V) kontrolü |
| 24 | [Marxlow ZD-30C 30 W Havya](https://www.robotistan.com/havya) | 1 | 325,01 | Pertinaks ve pompa kablosu lehimi |
| 25 | [ZD-10A Kalem Havya Standı](https://www.robotistan.com/havya-standi) | 1 | 155,53 | |
| 26 | [Kurtel Sn60/Pb40 Lehim Teli (100 gr) 1 mm](https://www.robotistan.com/kurtel-sn60-pb40-lehim-teli-100-gr-makara-1-mm) | 1 | 434,55 | Hırdavatta daha küçük makara daha ucuza bulunabilir |
| | **Alet toplamı** | | | **≈ 1.213,85** |

### 2.4 Özet

| Grup | Tutar (TL) |
| :--- | --: |
| Çekirdek elektronik | 1.874,57 |
| Bağlantı ve montaj | 1.097,07 |
| **Robotistan ara toplam** | **≈ 2.971,64** |
| Alet (evde yoksa) | 1.213,85 |
| **Alet dahil** | **≈ 4.185,49** |

Ara toplam 1.500 TL'nin üstünde olduğu için kargo ücretsizdir.

**Robotistan'da tükenmiş veya bulunmayanlar (20.10.2026):** kapasitif toprak nem sensörü, su geçirmez DS18B20, 8×5 mm hortum, 22AWG montaj kablosu, 2600'lük direnç seti.

## 3. Robotistan dışı tek kalem

| Kalem | Kaynak | Alınacak | Birim (TL) | Toplam (TL) | Not |
| :--- | :--- | :-: | --: | --: | :--- |
| [Kapasitif Toprak Nem Sensörü - Higrometre](https://www.direnc.net/kapasitif-toprak-nem-sensoru) | direnc.net (20.10.2026 stokta) | **6** (4 + 2 yedek) | 50,56 | 303,36 | 3,3–5,5 V, üzerinde regülatör var. Çıkış 0–3 V, yani UNO Q analog girişleri için güvenli |

**Sipariş durumu (9 Kasım 2026): henüz verilmedi.** E1, E2 ve E5 bu sensörlere bağlıdır; sipariş günü belli olunca tarihler güncellenir.

**Neden dışarıdan:** Robotistan'da yalnızca rezistif toprak sensörleri var. Rezistif problar 2,5 ayda korozyona uğrar ve README'deki "korozyona dayanıklı kapasitif sensör" iddiasını bozar. Kart kenarları ve üstteki elektronik oje veya makaronla kaplanır.

## 4. Yerel temin

| Kalem | Adet | Nereden | Not |
| :--- | :-: | :--- | :--- |
| Kasa (~60 × 40 × 20 cm) | 2 (özdeş) | Balıkçı (strafor), pazar, ambalajcı, Trendyol | Bkz. §7 |
| Naylon astar + drenaj tepsisi | 2 | Hırdavat / market | Süzülen suyu ölçmek için tepsi |
| Bidon, 20 L, ışık geçirmeyen, kapaklı | 2 | Hırdavat | Şamandıra kapağa ya da yan duvara monte edilir |
| Hortum **8 × 5 mm** (iç çap 5 mm) | ~5 m | Akvaryumcu | Pompa çıkışı 7,5 mm. Robotistan'ın pompaya önerdiği ölçü budur (orada tükenmiş) |
| Hortum 4/6 mm + redüksiyon + T-parça | ~5 m + birkaç adet | Akvaryumcu | YF-S401 girişi ve damlatıcı hattı. Redüksiyon ölçüsü ürünler gelince ölçülerek alınır |
| Damlatıcı veya kılcal boru | 2 set | Akvaryumcu / ziraat bayi | |
| Toprak, torf, perlit | 2 yatak için tek torba karışım | Fidancı / ziraat bayi | İki yatak aynı karışımla doldurulur |
| Turp veya roka tohumu | 2 paket (Tur 1 + Tur 2) | Ziraat bayi | |
| Kapaklı plastik saklama kabı (~2 L) | 1 (+1 yedek) | Market / züccaciye | Elektronik kutusu (proje kutusu yerine) |
| Şeffaf PE örtü ya da mini balkon serası | 1 | Hırdavat / Idefix | Yağmur koruması, bkz. §8 |
| Radyasyon kalkanı için beyaz, havalandırmalı küçük kap | 1 | Market | DHT22 doğrudan güneşte yanlış okur |
| Şeffaf oje veya silikon | 1 | Market / hırdavat | Kapasitif sensör kenarları ve kablo girişleri |
| Mezür (1 L, ml işaretli) | 1 | Market | Akış sensörü kalibrasyonu |
| Mutfak terazisi (1 g hassasiyet) | 1 | Evde ya da market | Gravimetrik kalibrasyon (E1) |
| USB-C şarj aleti (5 V 3 A / en az 15 W) ve kablo | 1 | Evde | UNO Q beslemesi |

## 5. Sadeleştirme ve gerekçeleri

| Çıkan | Yerine | Başvuruya etkisi |
| :--- | :--- | :--- |
| **HC-SR04 ×2** ve 2 gerilim bölücüsü | Depo hacmi **akış sensörünün saydığı hacimden** hesaplanır (başlangıç hacmi − toplam akış). Her dolumda bidon işaretinden veya mezürle elle sıfırlanır. Alt sınır kilidi şamandırada kalır | Plan zaten "akış birincil, seviye kaba kontrol" diyordu. Doğrulama zincirinde akış ve toprak tepkisi korunur |
| **TEMT6000** | MPU, **Open-Meteo**'dan güneş radyasyonu ve ET₀ alır. İnternet yoksa DHT22 sıcaklığıyla **Hargreaves** (FAO-56) yöntemine düşer | Buharlaşma tahmini FAO'nun kendi girdisine dayanır; yerel ölçüm DHT22 ile sürer |
| **12 V 2 A adaptör + LM2596** | UNO Q evdeki USB-C şarj aletinden, pompa ve sensörler 5 V 2 A adaptörden beslenir | Ayar gerektiren voltaj düşürücü kalkar; VIN pini belirsizliği ortadan kalkar |
| **Proje kutusu** | Kapaklı plastik saklama kabı | Daha ucuz, sudan daha iyi korur |
| **AJ-SR04M** (yedek) | — | Ultrasonik sensör kullanılmıyor |

**Dokunulmayanlar:** 4 kapasitif sensör (iki derinlik, çapraz doğrulama), iki ayrı bidon (A/B su bütçesinin fiziksel olarak gösterilmesi), akış sensörü ve şamandıra (doğrulanmış aktüasyon ve donanımsal emniyet).

## 6. Bağlantı ve güç planı

```text
USB-C şarj aleti (5 V 3 A) ──> UNO Q USB-C

5 V 2 A adaptör ─> Barrel jack ─┬─> Pompa A (+) ─ LR7843 A ─ GND   [1N5819 pompa uçlarına ters]
                                ├─> Pompa B (+) ─ LR7843 B ─ GND
                                └─> YF-S401 A/B VCC
Ortak GND: 5 V adaptör GND'si ile UNO Q GND'si birleştirilir (akış sinyali için şart)
UNO Q 3,3 V ──> kapasitif sensörler ×4, DHT22
```

| UNO Q pini | Bağlantı | Not |
| :--- | :--- | :--- |
| A0, A1 | Yatak A toprak nemi (5 cm / 10 cm) | 3,3 V ile besle; çıkış 0–3 V |
| A2, A3 | Yatak B toprak nemi (5 cm / 10 cm) | |
| A4, A5 | Boş (yedek / 3. yatak) | |
| D2, D3 | YF-S401 A / B darbe çıkışı | Kesme (interrupt) pinleri. 5 V darbe → 10k/20k bölücü → ≈ 3,3 V |
| D4, D5 | Şamandıra A / B | INPUT_PULLUP; şamandıra GND'ye kapatır |
| D10, D11 | LR7843 A / B PWM girişi | Açılışta LOW (pompa kapalı) |
| D12 | DHT22 veri | Modül tipi; pull-up kartın üzerinde |

> **UNO Q gerilim uyarısı:** MCU tarafı 3,3 V mantıktadır. Analog girişlere 3,3 V'tan yüksek gerilim uygulanmamalı. Dijital pinlerin 5 V toleransı resmi datasheet ile doğrulanana kadar akış darbe hatlarında bölücü kullanılır. Bölücü çıkışı, sensör UNO Q'ya bağlanmadan önce multimetreyle ölçülür.

**İlk kez kuranlar için sıra:** her modül önce breadboard üzerinde tek başına denenir (önce multimetreyle gerilim kontrolü, sonra kod). Pompa ve şamandıra timsah kabloyla denenir. Hepsi çalıştıktan sonra pertinaksa lehimlenir ve klemenslerle kutuya taşınır.

## 7. Kasa (test yatağı) temini

60 × 40 cm Avrupa standart kasa ölçüsüdür. **Ölçünün tam tutması şart değil:** karar katmanı mm biriminde çalıştığı için önemli olan iki yatağın **özdeş** olması ve iç alanın ölçülüp koda girilmesidir.

| Kaynak | Not |
| :--- | :--- |
| Balıkçı (strafor balık kasası) | Genelde ~60 × 40, ücretsiz veya çok ucuz. Yalıtımlı, kök bölgesi sıcaklığını dengeler. Naylon astar + drenaj deliği gerekir; yıkanmalı |
| Pazar / hal (plastik sebze kasası) | Delikliyse naylon astarla kullanılır |
| Trendyol "60x40 plastik kasa" | Ör. 60×40×20 katlanır kasa ~1.150 TL; 40×60×30 kapalı kasa ~840 TL (17.10.2026) |
| Hırdavat / ambalaj toptancısı ("Euro kasa", "stok kasası") | Kapalı plastik kasa, adet bazında |

- Tabana 6–8 adet drenaj deliği açılır. Altına tepsi konursa **süzülen su (D)** ölçülebilir; su dengesi için ek veri olur.
- Toprak: iki yatağa aynı torbadan, aynı karışım (ör. bahçe toprağı + torf + perlit), aynı sıkılıkta konur.

## 8. Balkon kurulumu — Adana

- **Yağmur deneyi bozar.** Yağmur ölçülmeyen bir su girdisidir (P); su bütçesini ve A/B karşılaştırmasını geçersiz kılar. Adana'da yağışlı dönem Kasım–Şubat'tır ve Tur 2 (Aralık) tam bu döneme denk gelir. Yataklar yağmur almamalı:
  - saçak / kapalı balkon bölümü, **veya**
  - şeffaf PE / polikarbonat örtü (yanları havalandırmalı), **veya**
  - raflı mini balkon serası (~2.000 TL; ılık havada kapağı açık tutulmalı, aşırı ısınmaya dikkat).
- **Elektronik:** saklama kabı yağmur ve doğrudan güneş almayan yere konur; kablo girişleri silikonla kapatılır, kablolar kaba aşağıdan girer (damla döngüsü). Priz kaçak akım korumalı olmalı.
- **Depolar:** ışık geçirmeyen ve kapaklı bidon (yosun, sivrisinek, yağmur suyu girişi). Şamandıra bidona monte edilir; her dolumda bidonun yanına çizilen litre işaretleriyle depo hacmi elle kaydedilir.
- **Sıcaklık ve ışık:** Adana'da don riski düşük; turp ve roka sonbaharda iyi gelişir. Ekim'de öğle güneşi yatakları hızla kurutabilir: güneye bakan balkonda README'deki iç mekân varsayımı (1–3 mm/gün) aşılabilir, Aralık'ta ise ~1 mm/gün civarına düşmesi beklenir (tahmin). E2 kuruma deneyiyle kalibre edilmeli; kontrol yatağının zamanlayıcı dozu buna göre ayarlanır.
- **Sensör yerleşimi:** DHT22 iki yatağın ortasına, gölgelikli bir radyasyon kalkanı içine (beyaz, havalandırmalı küçük kap) yerleştirilir; doğrudan güneşte yanlış yüksek sıcaklık okur.

## 9. Hazırlık takvimi (güncel)

> Önceki 17 Ekim – 7 Kasım takvimi geçerliliğini yitirdi. Güncel görev ve tarihler Notion görev tahtasında tutulur; özeti aşağıdadır. İki tur korunur; **Tur 1 kısaltıldı** (15 Kasım – 3 Aralık, README §9.2).

| Dönem | Donanım ve tesisat | Yazılım |
| :--- | :--- | :--- |
| **9–15 Kasım** | Siparişi say ve kontrol et; direnc.net siparişini ver; UNO Q + App Lab kurulumu, Bridge testi (**M0**); pin 5 V toleransını doğrula; pompa, akış, şamandıra, DHT22 breadboard testi; kasa, bidon, toprak, tohum, hortum temini; balkonda yağmur korumalı alan; **15 Kasım Tur 1 ekim** (sensörler gelene kadar mezürle elle sulama ve kayıt) | MCU ↔ MPU mesaj şeması (JSON alanları, birimler, olay tipleri); depo iskeleti (`firmware/`, `app/`, `simulation/`) |
| **16–22 Kasım** | Kapasitif sensör iki noktalı + gravimetrik kalibrasyon (**E1**, ≈ 18 Kasım); pompa debisi ve YF-S401 darbe/litre kalibrasyonu; MCU güvenlik kilitleri ve **E3** (≈ 21 Kasım); pertinaksa geçiş ve kutulama; **MVP 22 Kasım** | MCU: örnekleme + medyan filtre, pompa sürücü, akıştan depo hacmi. MPU: veri alma + SQLite, Open-Meteo istemcisi, simülatör ilk sürüm, kural tabanlı politika, pano ilk sürüm |
| **23 Kasım – 3 Aralık** | Tur 1 kural tabanlı sulama ile sürer; **E2** kuruma eğrileri (19 Kasım – 3 Aralık, Tur 1 yataklarında); **E4** anomali enjeksiyonu (≈ 30 Kasım); 3 Aralık'ta dondurma, yatakların boşaltılması | Model v1, model Tur 1'de gölge modda (≈ 28 Kasım – 3 Aralık), anomali tespiti, bütçe politikası, pano (karar gerekçesi), senaryo motoru |
| **4–27 Aralık** | **Tur 2** ekim ve **E5** A/B deneyi | Dokümantasyon, video |

Sorumlular ekip içinde belirlenir (Notion tahtasında sorumlu alanı boş bırakılmıştır).

## 10. Açık noktalar

- [ ] direnc.net kapasitif sensör siparişi (6 adet) henüz verilmedi; sipariş günü ve teslim tarihi netleşince E1 ve MVP tarihleri güncellenecek
- [ ] UNO Q dijital pinlerinin 5 V toleransının ve USB-C güç gereksiniminin resmi datasheet'ten doğrulanması
- [ ] Pompa çıkışı (7,5 mm) ile YF-S401 bağlantı ağzı arasındaki redüksiyon ölçüsü (parçalar geldi, ölçülecek)
- [ ] YF-S401'in 3,5 mm girişinin pompa debisini ne kadar kıstığı: ilk iş debi ölçülür; 0,3 L/dk altına düşerse sensör alt sınırın dışında kalır
- [ ] Balkonun yönü ve yağmurdan korunan alanın boyutu
- [ ] Elde havya, multimetre ve lehim teli olup olmadığı (§2.3)
- [ ] Yayın için GitHub deposu ve lisans (kaynak kod MIT, dokümantasyon ve veri CC BY 4.0 önerildi)

## Kaynaklar

- Robotistan ürün sayfaları (20.10.2026): tablolardaki bağlantılar
- Kapasitif sensör: [direnc.net](https://www.direnc.net/kapasitif-toprak-nem-sensoru)
- YF-S401 teknik bilgi: [DFRobot wiki](https://wiki.dfrobot.com/sen0216/)
- UNO Q pin gerilimleri (üçüncü taraf, doğrulanmalı): [etechnophiles](https://www.etechnophiles.com/?p=22458) · [52Pi](https://docs.52pi.com/md/kz-0092/kz-0092/)
- Hava verisi: [Open-Meteo](https://open-meteo.com/) (radyasyon, ET₀) · Hargreaves yöntemi: FAO-56, Bölüm 3
- Kasa: [Trendyol 40×60](https://www.trendyol.com/40-x-60-sepet-x-c104221-a92-v23999) · Mini sera: [Idefix](https://www.idefix.com/missidea-portatif-balkon-ve-bahce-bitki-yetistirme-serasi-p-20704716)
