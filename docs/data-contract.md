# DRAFT — Ekip onayı bekleniyor

Aysima'nın teknik incelemesi ve onayı bekleniyor.

# Suİz — MCU/MPU Veri Sözleşmesi (TASLAK v0.1)

**Durum:** Öneri; Hilal ve Aysima onayı bekliyor. **Kaynak:** README.md §5, §7 ve mevcut mock üreticisinin raporlanan çıktısı. Bu belge, canlı depoya henüz eklenmedi.

## 1. Sınırlar
- MCU (C++): sensörleri okur, ham ölçüm ve güvenlik olaylarını iletir; pompa üzerinde nihai kontrol MCU'dadır.
- MPU (Python): veri kabulü/doğrulama, zaman damgası, kalibrasyon, SQLite kaydı, tahmin ve karar üretimi.
- Bridge (RPC): MCU/MPU arasında taşıma. Buradaki JSON şeması **mantıksal kayıt modeli**dir; RPC'nin gerçek tipleri/metotları UNO Q üzerinde doğrulanacaktır.
- Her kaynak (`mock`, `mcu`) ortak bir Python iç modeli üretir. Mock veriler gerçek deney sonuçları olarak raporlanmaz.

## 2. İşlenmiş ölçüm kaydı (MPU iç model, geçici)
```json
{
  "schema_version": "1.0",
  "message_type": "sensor_reading",
  "timestamp": "2026-11-21T06:00:00Z",
  "bed_id": "A",
  "source": "mock",
  "is_synthetic": true,
  "air_temperature_c": 20.5,
  "relative_humidity_pct": 64.0,
  "soil": [
    {"depth_cm": 5, "raw_adc": 2022, "moisture_pct": 31.0, "status": "normal"},
    {"depth_cm": 10, "raw_adc": null, "moisture_pct": null, "status": "disconnect"}
  ]
}
```

### Alan kuralları
- `bed_id`: `A` veya `B`.
- `timestamp`: MPU tarafından atanabilen UTC ISO 8601 zaman damgası; MCU zaman kaynağı ayrıca kararlaştırılacak.
- `source`: `mock` veya `mcu` (gerektiğinde genişletilebilir).
- `is_synthetic`: `source=mock` ise `true`, gerçek cihazdan geliyorsa `false`. SQLite'a aynen kaydedilir.
- `soil`: derinlikler 5 ve 10 cm; sıralamaya güvenilmez, `depth_cm` ile eşleşilir.
- `raw_adc`: sıfır veya pozitif tamsayı ya da `null`; gerçek ADC çözünürlüğü doğrulanana kadar üst sınır belirtilmez.
- `moisture_pct`: kalibre edilmişse 0–100 arası sayı; kalibrasyon yoksa `null`. Örnek mock yüzdesi gerçek ölçüm değildir.
- `status`: ilk mock testleri için `normal | spike | stuck | disconnect`. Üretim sisteminde bunlar arasında hangilerinin MCU'dan, hangilerinin MPU anomali katmanından geldiği netleştirilecek.
- `air_temperature_c` ve `relative_humidity_pct`: DHT22 ortak sensördür; aynı zamanda birden fazla yatak kaydı oluşturulursa tekrar edebilir. Eksik veri durumunda `null` yönetimi ayrıca test edilmelidir.
- İleride gerçek veri modeli değişirse `schema_version` yükseltilir; sessiz alan yeniden adlandırma yapılmaz.

## 3. Geçiş ilkesi
Mevcut `suiz.mock-sensors.provisional.v1` şeması korunabilir. `simulation` verisini yukarıdaki iç kayda dönüştüren tek bir adapter yazılır; `app/ingest` aynı iç kaydı gerçek MCU adaptöründen de alır.

## 4. Sonraki mesaj türleri — henüz uygulanmayacak
- `irrigation_request`: MPU isteği (yatak, istenen su hacmi, komut kimliği); son yetki MCU'da.
- `irrigation_result`: MCU'nun gerçekte uyguladığı eylem, akış doğrulaması, ret nedeni.
- `safety_event`: depo düşük, akış yok, maksimum süre, bağlantı/heartbeat sorunu.
- Akış darbe sayacının sıfırlama biçimi, paket/olay kimliği, yeniden gönderim ve idempotency ayrıca belirlenecek.

## 5. Kabul kriterleri
1. Aynı seed ile mock kayıtları tekrar üretilebilir.
2. `A/B` ve `5/10 cm` kayıtları doğru ayrılır.
3. Kopmada `raw_adc=null`, `moisture_pct=null`; sayısal değer olmayan veri karar algoritmasına normal ölçüm diye aktarılmaz.
4. `is_synthetic` SQLite'a ve CSV'ye taşınır; gerçek deney raporundan ayrılır.
5. Üretilen kayıtlar ortak Python doğrulama katmanından geçer.
6. Gerçek Bridge örneği geldiğinde onun çıktısı adapte edilir; simülatör ve depolama modülü yeniden yazılmaz.

## 6. Ekip onayı bekleyen noktalar
- UNO Q ADC çözünürlüğü/analog okuma aralığı (donanım testi)
- Bridge RPC metotları ve taşıma tipi (Aysima PoC)
- `timestamp` sahipliği ve MCU monoton zaman bilgisi
- `status` kaynağı (ölçüm arızası mı MPU anomali sonucu mu)
- Akış, şamandıra ve pompa olaylarının ayrı sözleşmesi

**Not:** AGENTS.md uyarınca teknik karar değişiklikleri Notion ana dokümanı ile eşleştirilir; görev durumu yalnız Notion'da tutulur. Ekip onayı gelmeden bu taslak resmi karar diye sunulmaz.


## Mevcut uygulamayla farklar

Bu bölüm, taslağı `feature/mock-storage-integration` dalındaki `b2b7553` uygulamasıyla karşılaştırır. Yukarıdaki teknik öneriler ekip incelemesine açıktır.

- **Donma durumu.** Taslak `stuck` değerini önerir. Mock üreticisi aynı senaryo için `freeze` yayımlar. Ortak adlandırma ekip kararı bekler.
- **Kayıt yapısı.** Mock, `schema: "suiz.mock-sensors.provisional.v1"` alanını ve derinliğe göre gruplanmış `soil` listesini kullanır. Taslak örneği `schema_version` ve `message_type` alanlarını önerir. Mevcut adapter, ham ADC ve nem yüzdesini `soil_5cm_adc` ve `soil_5cm_pct` gibi düz `Measurement.sensors` kanallarına dönüştürür.
- **Kaynak ve UTC gösterimi.** Mock mesajı `source` taşımaz. Adapter bu alanı ekler ve varsayılan olarak `mock-sensors` kullanır. Taslak örneğinde kaynak `mock` olarak gösterilir. Taslaktaki `Z` ve mock çıktısındaki `+00:00` aynı UTC ofsetini gösterir.
- **Tekrar üretilebilirlik.** Aynı kayıt dizisi için seed, başlangıç zamanı ve üretim ayarları aynı olmalıdır. Ayarlara örnekleme aralığı, yatak seçimi ve sırası, örnek sayısı ile sulama ve arıza senaryoları dahildir.
- **CSV dışa aktarımı.** Mevcut entegrasyon `is_synthetic` alanını SQLite'a kaydeder. CSV dışa aktarımı henüz geliştirilmedi.
- **Teknik eksik — `status` kaydı.** Ölçüm modelinde metinsel durum etiketi için alan bulunmadığından adapter `status` bilgisini SQLite'a aktarmaz. Kopmada `raw_adc` ve `moisture_pct` değerleri `null` olarak saklanır. Durum bilgisinin kaynağı ve nerede saklanacağı ekip kararı bekler.
