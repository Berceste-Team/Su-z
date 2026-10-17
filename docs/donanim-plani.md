# Suİz — Donanım Temin ve Hazırlık Planı

> Hazırlayan: donanım ve tesisat sorumlusu · Tarih: 17 Ekim 2026
> Fiyatlar 17.10.2026'da robotistan.com'da görülen KDV dahil liste fiyatlarıdır; sipariş öncesi tekrar kontrol edilmelidir.

## 1. Kapsam ve varsayımlar

| Konu | Karar |
| :--- | :--- |
| **Hazırlık süresi** | 2–3 hafta (17 Ekim – ~7 Kasım). Bitki yetiştirme dahil toplam süre ~2,5 ay (30 Aralık'a kadar); README takvimi geçerli |
| **Konum** | Adana, balkon |
| **Temin kuralı** | Elektronik kalemlerin tamamı Robotistan'dan alınır. Dışarıdan alım yalnızca Robotistan'da hiç bulunmayan ve projenin çekirdek iddiasını etkileyen kalemler için yapılır (bkz. [Bölüm 4](#4-robotistan-dışı-istisnalar)) |
| **Bütçe** | 50 USD Robotistan hediye çeki (≈ 2.100–2.300 TL, kura göre). Çeki aşan kısım ekip tarafından yine Robotistan'dan karşılanır |
| **README'den sapmalar** | 12 V pompa yerine 6 V mini dalgıç pompa; BME280 yerine DHT22; BH1750 yerine TEMT6000; JSN-SR04T yerine HC-SR04. Gerekçeler aşağıda. README'nin 6. bölümü bu belgeye göre güncellenmeli |

## 2. Robotistan sipariş listesi

### 2.1 Çekirdek (hediye çeki ile)

| # | Ürün (Robotistan adı) | Adet | Birim (TL) | Toplam (TL) | Rolü / not |
| :-: | :--- | :-: | --: | --: | :--- |
| 1 | Su Akış Sensörü YF-S401 Debimetre 0.3-6L/Min 3.5mm | 2 | 225,85 | 451,70 | Yatak başına akış ve hacim doğrulama. Pompanın debisi (~1–2 L/dk) ölçüm aralığında |
| 2 | Mini Dalgıç Su Pompası 6V 120 Litre/Saat | 3 | 49,99 | 149,97 | Yatak başına 1 pompa + 1 yedek. 5–6 V ile çalışır |
| 3 | LR7843 MOSFET Sürücü Kartı | 2 | 48,78 | 97,56 | Pompa sürme; optokuplörlü giriş, 3,3 V tetikleme |
| 4 | Su Seviye Sensörü (91x24 mm) - ZP7510 | 2 | 145,14 | 290,28 | Şamandıra; yazılımdan bağımsız düşük seviye kilidi |
| 5 | HC-SR04 Ultrasonik Mesafe Sensörü | 2 | 63,24 | 126,48 | Depo seviyesi (kaba kontrol). Echo hattına gerilim bölücü |
| 6 | DHT22 Sıcaklık ve Nem Sensörü | 1 | 106,60 | 106,60 | Ortam sıcaklık/nem, VPD hesabı |
| 7 | CJMCU-TEMT6000 Ortam Işığı Sensörü | 1 | 75,88 | 75,88 | Işık düzeyi (analog) |
| 8 | GePro UM-0285, 12 V 2 A Adaptör | 1 | 208,38 | 208,38 | Tek besleme: UNO Q VIN + pompa hattı |
| 9 | LM2596 Mini Ayarlanabilir Voltaj Düşürücü 3A | 1 | 68,66 | 68,66 | 12 V → 5,5 V (pompalar, akış, HC-SR04) |
| 10 | Klemens Girişli DC Barrel Jack | 1 | 9,64 | 9,64 | Adaptör girişi |
| 11 | 1N5819 Diyot | 4 | 2,95 | 11,80 | Pompa flyback koruması (2 kullanılır, 2 yedek) |
| 12 | 30 cm 40 Pin Dişi-Erkek Jumper Kablo | 1 | 59,62 | 59,62 | |
| 13 | 30 cm 40 Pin Erkek-Erkek Jumper Kablo | 1 | 63,84 | 63,84 | |
| 14 | 30 cm 40 Pin Dişi-Dişi Jumper Kablo | 1 | 56,61 | 56,61 | |
| 15 | KF2EDGR-5.08-2P / 3P Geçmeli Klemens | 4 + 4 | 7,89 / 11,26 | 76,60 | Sensör ve güç bağlantıları |
| | **Çekirdek toplam** | | | **≈ 1.853,62** | 1.500 TL üstü kargo ücretsiz |

### 2.2 Çek yeterse (öncelik sırasıyla)

| # | Ürün | Adet | Birim (TL) | Not |
| :-: | :--- | :-: | --: | :--- |
| 16 | 113 x 197.4 x 63 Proje Kutusu (Siyah) | 1 | 324,25 | Elektronik kutusu. IP sınıfı yok; kablo girişleri silikonla kapatılıp kutu yağmur almayan yere konur |
| 17 | Direnç seti / 10 kΩ + 20 kΩ dirençler | — | fiyat bakılmadı | Echo ve akış darbe hatları için 5 V → 3,3 V bölücü (lojik seviye dönüştürücü tükenmiş) |
| 18 | Breadboard / delikli pertinaks | 1 | fiyat bakılmadı | Kalıcı kurulumda pertinaks + lehim tercih edilir |
| 19 | AJ-SR04M Su Geçirmez Ultrasonik Sensör | 2 | 215,78 | HC-SR04 nem nedeniyle sorun çıkarırsa yedek; kör bölgesi ~20 cm |

**Robotistan'da tükenmiş veya bulunmayan kalemler (17.10.2026):** kapasitif toprak nem sensörü, su geçirmez DS18B20, BH1750, lojik seviye dönüştürücü, IP67 contalı kutular, hortum.

### 2.3 Neden bu seçimler?

- **6 V pompa:** Robotistan'da 1–2 L/dk debili 12 V dalgıç pompa yok. 6 V/120 L/sa pompa hem debi hem güvenlik açısından uygun. Yedek almak ucuz olduğu için 3 adet.
- **DHT22 (BME280 yerine):** VPD hesabı için sıcaklık ve bağıl nem yeterli; basınca gerek yok. Fark ≈ 330 TL.
- **HC-SR04 (JSN-SR04T yerine):** Akış sensörü birincil hacim ölçümü olduğu için seviye ölçümü yalnızca kaba kontrol. HC-SR04'ün kör bölgesi (~2 cm) 20 L bidon için daha uygun. Su geçirmez modellerin 20–25 cm kör bölgesi var. Sensör depo kapağına, su yüzeyine bakacak şekilde, yağmur almayan yere monte edilir.
- **TEMT6000 (BH1750 yerine):** BH1750 Robotistan'da yok. Analog çıkış A4'e bağlanır.
- **Tek 12 V adaptör:** UNO Q, VIN girişinden 7–24 V ile beslenebilir (README §6). Pompalar 5,5 V'a düşürülmüş ayrı bir hattan beslenir. Pompa akımı (~2 × 0,3 A) 2 A'lık adaptör için yeterli pay bırakır. *VIN pini ve kartın akım çekişi kart dokümanından doğrulanmalı.*

## 3. Bağlantı ve güç planı (taslak)

```text
12 V 2 A adaptör ─┬─> UNO Q VIN
                  └─> LM2596 (5,5 V) ─┬─> Pompa A (+) ─ LR7843 A ─ GND   [1N5819 pompa uçlarına ters]
                                      ├─> Pompa B (+) ─ LR7843 B ─ GND
                                      ├─> YF-S401 A/B VCC
                                      └─> HC-SR04 A/B VCC
Ortak GND: adaptör, LM2596, UNO Q, tüm sensörler
```

| UNO Q pini | Bağlantı | Not |
| :--- | :--- | :--- |
| A0, A1 | Yatak A toprak nemi (5 cm / 10 cm) | 3,3 V ile besle; çıkış ≤ 3,3 V |
| A2, A3 | Yatak B toprak nemi (5 cm / 10 cm) | |
| A4 | TEMT6000 | 3,3 V ile besle |
| A5 | Boş (yedek / 3. yatak) | |
| D2, D3 | YF-S401 A / B darbe çıkışı | Kesme (interrupt) pinleri. 5 V darbe → bölücü |
| D4, D5 | Şamandıra A / B | INPUT_PULLUP; şamandıra GND'ye kapatır |
| D6, D7 / D8, D9 | HC-SR04 A / B trig, echo | Echo → 10k/20k bölücü |
| D10, D11 | LR7843 A / B PWM girişi | Açılışta LOW (pompa kapalı) |
| D12 | DHT22 veri | 3,3 V, 10 kΩ pull-up |

> **UNO Q gerilim uyarısı:** MCU tarafı 3,3 V mantıktadır. A0–A5 analog girişlerine 3,3 V'tan yüksek gerilim uygulanmamalı. Bazı kaynaklar dijital pinlerin 5 V toleranslı olduğunu söylüyor, ancak kaynaklar çelişkili. Resmi datasheet kontrol edilene kadar her 5 V çıkışlı sinyale bölücü konur.

## 4. Robotistan dışı istisnalar

| Kalem | Neden dışarıdan | Öneri |
| :--- | :--- | :--- |
| **Kapasitif toprak nem sensörü v1.2 (4 + 2 yedek)** | Robotistan'da yalnızca **rezistif** sensörler var ("Toprak Nemi Algılama Sensörü", 49,99 TL; "12V Toprak Hygrometer", röle çıkışlı). "SHT10 Soil" (1.401 TL) toprak nemini değil, prob içindeki hava nemini ölçüyor. Rezistif problar 2,5 ayda korozyona uğrar ve README'nin "korozyona dayanıklı kapasitif sensör" iddiasını bozar | Kapasitif v1.2 modülü (ör. direnc.net). Mümkünse TLC555 entegreli olanlar seçilir (3,3 V'ta çalışır). Kart kenarları ve üstteki elektronik oje veya makaronla kaplanır |
| **Tesisat ve mekanik** (README §6'da zaten yerel temin olarak planlı) | Robotistan'da hortum tükenmiş; kasa, depo, toprak ve tohum satılmıyor | Akvaryumcu: 4/6 mm silikon hortum, redüksiyonlar, damlatıcı veya kılcal boru. Hırdavat: 20 L ışık geçirmeyen kapaklı bidon ×2 |

Robotistan'da kapasitif sensör stoğa girerse bu istisna kaldırılır. Rezistif sensörü yalnızca acil yedek olarak düşünün: ölçüm anında GPIO ile beslenmeli, ölçüm dışında kapalı tutulmalı.

## 5. Kasa (test yatağı) temini

60 × 40 cm Avrupa standart kasa ölçüsüdür. **Ölçünün tam tutması şart değil:** karar katmanı mm biriminde çalıştığı için önemli olan iki yatağın **özdeş** olması ve iç alanın ölçülüp koda girilmesidir.

| Kaynak | Not |
| :--- | :--- |
| Balıkçı (strafor balık kasası) | Genelde ~60 × 40, ücretsiz veya çok ucuz. Yalıtımlı, kök bölgesi sıcaklığını dengeler. Naylon astar + drenaj deliği gerekir; yıkanmalı |
| Pazar / hal (plastik sebze kasası) | Delikliyse naylon astarla kullanılır |
| Trendyol "60x40 plastik kasa" | Ör. 60×40×20 katlanır kasa ~1.150 TL; 40×60×30 kapalı kasa ~840 TL |
| Hırdavat / ambalaj toptancısı ("Euro kasa", "stok kasası") | Kapalı plastik kasa, adet bazında |

- Tabana 6–8 adet drenaj deliği açılır. Altına tepsi konursa **süzülen su (D)** ölçülebilir; su dengesi için ek veri olur.
- Toprak: iki yatağa aynı torbadan, aynı karışım (ör. bahçe toprağı + torf + perlit), aynı sıkılıkta konur.

## 6. Balkon kurulumu — Adana

- **Yağmur deneyi bozar.** Yağmur ölçülmeyen bir su girdisidir (P); su bütçesini ve A/B karşılaştırmasını geçersiz kılar. Adana'da yağışlı dönem Kasım–Şubat'tır ve Tur 2 (Aralık) tam bu döneme denk gelir. Yataklar yağmur almamalı:
  - saçak / kapalı balkon bölümü, **veya**
  - şeffaf PE / polikarbonat örtü (yanları havalandırmalı), **veya**
  - raflı mini balkon serası (~2.000 TL; ılık havada kapağı açık tutulmalı, aşırı ısınmaya dikkat).
- **Elektronik:** proje kutusu yağmur ve doğrudan güneş almayan yere konur; kablo girişleri silikonla kapatılır, kablolar kutuya aşağıdan girer (damla döngüsü). Priz kaçak akım korumalı olmalı.
- **Depolar:** ışık geçirmeyen ve kapaklı bidon (yosun, sivrisinek, yağmur suyu girişi). Şamandıra ve HC-SR04 kapağa monte edilir.
- **Sıcaklık ve ışık:** Adana'da don riski düşük; turp ve roka sonbaharda iyi gelişir. Ekim'de öğle güneşi yatakları hızla kurutabilir: güneye bakan balkonda README'deki iç mekân varsayımı (1–3 mm/gün) aşılabilir, Aralık'ta ise ~1 mm/gün civarına düşmesi beklenir (tahmin). E2 kuruma deneyiyle kalibre edilmeli; kontrol yatağının zamanlayıcı dozu buna göre ayarlanır.
- **Sensör yerleşimi:** DHT22 ve TEMT6000 iki yatağın ortasına, gölgelikli bir radyasyon kalkanı içine (beyaz, havalandırmalı küçük kap) yerleştirilir; doğrudan güneşte DHT22 yanlış yüksek sıcaklık okur.

## 7. Hazırlık takvimi (17 Ekim – 7 Kasım)

| Hafta | Donanım ve tesisat | Yazılım (3 kişi) |
| :--- | :--- | :--- |
| **1 · 17–24 Ekim** | Robotistan siparişi (hemen); kapasitif sensör siparişi; kasa, bidon, toprak, tohum, hortum temini. UNO Q + App Lab kurulumu, Bridge "merhaba" testi (**M0**) | MCU ↔ MPU mesaj şemasının (JSON alanları, birimler, olay tipleri) birlikte sabitlenmesi; depo iskeleti (`firmware/`, `app/`, `simulation/`) |
| **2 · 25–31 Ekim** | Sensörlerin tek tek bağlanması; kapasitif sensör iki noktalı kalibrasyon (kuru / doygun) + gravimetrik kontrol (**E1**); pompa debisi ve YF-S401 darbe/litre kalibrasyonu (mezür ile); yatakların kurulması, bitkisiz kuruma eğrisinin (**E2**) başlatılması | MCU: örnekleme + medyan filtre, pompa sürücü. MPU: veri alma + SQLite kaydı. Simülatör ilk sürüm |
| **3 · 1–7 Kasım** | MCU güvenlik kilitleri: kuru çalışma, akış yok (3 sn), azami süre (60 sn), heartbeat (**E3** ilk tur); kablo düzeni ve kutulama; **5 Kasım Tur 1 ekim** | Kural tabanlı politika uçtan uca (**M2 / MVP**); pano ilk sürüm (canlı değerler + son kararlar) |

**Önerilen iş bölümü**

| Kişi | Sorumluluk |
| :--- | :--- |
| Donanım sorumlusu | Devre, tesisat, kalibrasyon; MCU firmware'i ve güvenlik denetçisi |
| Yazılım 1 | Bridge veri alma, kayıt (SQLite/CSV), yerel pano |
| Yazılım 2 | Simülatör, bütçe politikası, tahmin ve anomali modeli, senaryo motoru |

## 8. Açık noktalar

- [ ] Hediye çekinin TL karşılığı ve kargo dahil olup olmadığı
- [ ] UNO Q VIN pini ve 3,3 V / 5 V tolerans değerlerinin resmi datasheet'ten doğrulanması
- [ ] Pompa çıkışı (~7–8 mm) ile YF-S401 bağlantı ağzı arasındaki redüksiyon ölçüsü (ürünler gelince ölçülecek)
- [ ] Balkonun yönü ve yağmurdan korunan alanın boyutu
- [ ] README §6 donanım tablosunun bu belgeye göre güncellenmesi

## Kaynaklar

- Robotistan ürün aramaları (17.10.2026): [akış sensörü](https://www.robotistan.com/arama?q=akis+sensoru) · [pompa](https://www.robotistan.com/arama?q=pompa) · [MOSFET](https://www.robotistan.com/arama?q=mosfet) · [seviye](https://www.robotistan.com/arama?q=seviye) · [HC-SR04](https://www.robotistan.com/arama?q=hc-sr04) · [sıcaklık/nem](https://www.robotistan.com/arama?q=sicaklik+nem+sensoru) · [ışık](https://www.robotistan.com/arama?q=isik+sensoru) · [LM2596](https://www.robotistan.com/arama?q=lm2596) · [adaptör](https://www.robotistan.com/arama?q=adaptor+12v) · [toprak](https://www.robotistan.com/arama?q=soil) · [proje kutusu](https://www.robotistan.com/arama?q=proje+kutusu)
- Robotistan rezistif sensörler: [Toprak Nemi Algılama Sensörü](https://www.robotistan.com/toprak-nemi-algilama-sensoru) · [12V Toprak Hygrometer](https://www.robotistan.com/nem-algilama-nem-izleme-modulu) · [SHT10 Soil](https://www.robotistan.com/sht10-sicaklik-ve-nem-sensoru)
- Kapasitif sensör: [direnc.net](https://www.direnc.net/kapasitif-toprak-nem-sensoru)
- YF-S401 teknik bilgi: [DFRobot wiki](https://wiki.dfrobot.com/sen0216/)
- UNO Q pin gerilimleri (üçüncü taraf, doğrulanmalı): [etechnophiles](https://www.etechnophiles.com/?p=22458) · [52Pi](https://docs.52pi.com/md/kz-0092/kz-0092/)
- Kasa: [Trendyol 40×60](https://www.trendyol.com/40-x-60-sepet-x-c104221-a92-v23999) · Mini sera: [Idefix](https://www.idefix.com/missidea-portatif-balkon-ve-bahce-bitki-yetistirme-serasi-p-20704716)
