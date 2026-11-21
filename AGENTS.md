# AGENTS.md — Suİz depo kuralları (insanlar ve AI agent'lar için)

Önce bunu okuyun, sonra düzenleme yapın.

## Tek veri kaynağı: proje sitesi

| Kaynak | Rolü |
| :--- | :--- |
| **Proje sitesi: [berceste-team.github.io/Su-z](https://berceste-team.github.io/Su-z/)** (kaynağı `docs/index.html`, şema `docs/sema/`) | Proje bilgisinin tek kaynağı: durum, takvim, kurulum, bağlantı şeması, sonuçlar |
| **`README.md` ve `docs/donanim-plani.md`** | Ayrıntılı teknik kayıt (proje şartnamesi; donanım ve tesisat). Siteyle aynı karar ve tarihleri içermelidir. Kod `firmware/`, `app/`, `simulation/` altına gelecek |
| **Notion — "Görevler" tahtası** | Yalnızca görevler (Yapılacak / Yapılıyor / Yapıldı). Proje bilgisi Notion'da tutulmaz; sayfada sitenin bağlantısı vardır. Görevler bu depoya kopyalanmaz |

## Kurallar

1. **Bir karar, takvim, donanım ya da deney değişikliği önce sitede (`docs/index.html`) yapılır**, aynı iş içinde `README.md` ve `docs/donanim-plani.md` de eşitlenir; yapamıyorsanız farkı kullanıcıya bildirin. Çelişki fark ederseniz sessizce birini seçmeyin, kullanıcıya sorun.
2. **Görev durumu yalnızca Notion tahtasındadır.** Görevler kısa ve net yazılır; tahtada yalnızca sıradaki adımların görevleri durur, ileri aşamaların kartları zamanı gelince eklenir. Depodaki "İlerleme" listesi kilometre taşı düzeyindedir.
3. **Tarihleri ve kararları gerekçesiyle yazın.** Örnek: takvim 15 Ocak'a uzatıldı (16 Kasım 2026), nedeni README §9.2'de.
4. Sorumlu alanı Notion'da bilerek boştur; ekip kendisi seçer, atama yapmayın.
5. Geçersiz bilgi eklemeyin: iddialar README'deki dürüst raporlama ilkelerine uymalıdır (sonuçlar olumsuz olsa da olduğu gibi raporlanır, istatistiksel anlamlılık iddia edilmez).
6. Commit ve push yalnızca kullanıcı istediğinde yapılır.
7. Şemanın kaynağı `tools/baglanti-semasi/gen2.py`'dir; çalıştırınca `tools/baglanti-semasi/index.html` ve `docs/sema/index.html` yazılır (ikisi aynı olmalı). Şema değişince PDF de (`Suiz-Baglanti-Semasi.pdf`) `out/b1…b8.svg` dosyalarından yeniden üretilir.

## Güncel durum (21 Kasım 2026)

- 21 Kasım 2026: MOSFET kartları lehimlendi, elektrik bağlantıları kuruldu; 5 V adaptörün fişi kesilip klemensle bağlandı (gelen klemensli jak erkek çıktı). Henüz güç verilmedi, hiçbir test yapılmadı. Yataklar hazırlanıyor; Tur 1 ekiminin 19 Kasım'da yapılıp yapılmadığı teyit edilmedi, takvim buna göre gözden geçirilecek.

- Robotistan siparişi ve 6 kapasitif nem sensörü (v2.0, HW-390, Robocombo) teslim alındı ve parçadan doğrulandı. Elde ayrıca dirençli tip sensörler var; deneyde kullanılmaz.
- **Kullanıcıya hatırlat (kendisi istedi, 16 Kasım 2026):** kapasitif nem sensörleri toprağa girmeden önce kart kenarlarına şeffaf oje sürülmeli, elektronik kısım oje ya da makaronla korunmalı. Bu iş yapıldığı teyit edilene kadar, sensörler ya da ekim konuşulduğunda ve her oturumun sonunda hatırlatın; yapılınca bu maddeyi silin. Aynı not şemanın nem sensörü adımında da yazar.
- MOSFET kartı (üç klemensli), akış sensörü, pompa ve şamandıra 16 Kasım'da parçalarla doğrulandı; şema ve dokümanlar düzeltildi (docs/donanim-plani.md §6.1).
- **İki tur korunur; takvim 15 Ocak 2027'de biter.** Tur 1: 19 Kasım – 13 Aralık (sensörler toprakta 24 Kasım; kural tabanlı sulama Yatak B 3 Aralık, Yatak A 8 Aralık; güvenlik testleri 9–11 Aralık); kod ve donanım 13 Aralık'ta donar; Tur 2 / E5 A/B deneyi 14 Aralık – 7 Ocak; analiz ve yayın 8–10 Ocak.
- 17 Kasım 2026: Notion ana dokümanındaki proje bilgisi kaldırıldı; Notion yalnızca görev tahtasıdır. Test yatağı kabı (kasa) henüz alınmadı; ölçüleri netleşince alan ve litre hesapları gözden geçirilecek.
