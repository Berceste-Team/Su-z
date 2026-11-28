# AGENTS.md — Suİz depo kuralları (insanlar ve AI agent'lar için)

Önce bunu okuyun, sonra düzenleme yapın.

## Tek veri kaynağı: proje sitesi

| Kaynak | Rolü |
| :--- | :--- |
| **Proje sitesi: [berceste-team.github.io/Su-z](https://berceste-team.github.io/Su-z/)** (kaynağı `docs/index.html`, şema `docs/sema/`) | Proje bilgisinin tek kaynağı: durum, takvim, kurulum, bağlantı şeması, sonuçlar |
| **`README.md` ve `docs/donanim-plani.md`** | Ayrıntılı teknik kayıt (proje şartnamesi; donanım ve tesisat). Siteyle aynı karar ve tarihleri içermelidir. Kod `app/`, `simulation/` ve `uno-q-app/` (App Lab uygulaması; MCU sketch'i `uno-q-app/sketch/`, 28 Kasım 2026 kararı, #17) altında durur |
| **[GitHub issue'ları](https://github.com/Berceste-Team/Su-z/issues)** | Görevler, düzeltmeler ve karar bekleyen konular (28 Kasım 2026'dan itibaren; Notion'un yerini aldı). Karar gerektiren issue'da karar ve gerekçesi issue'ya yazılır; atanan kişi işi o karara göre yapar ve PR açıklamasına `Closes #N` yazar |
| **Notion** | 28 Kasım 2026'dan beri görev tahtası olarak kullanılmıyor; açık görevler GitHub issue'larına taşındı, eski tahtalar donduruldu. Notion'da yalnızca ekip içi harcama tablosu tutulur; görev ya da proje bilgisi yazılmaz |

## Kurallar

1. **Bir karar, takvim, donanım ya da deney değişikliği önce sitede (`docs/index.html`) yapılır**, aynı iş içinde `README.md` ve `docs/donanim-plani.md` de eşitlenir; yapamıyorsanız farkı kullanıcıya bildirin. Çelişki fark ederseniz sessizce birini seçmeyin, kullanıcıya sorun.
2. **Görevler GitHub issue'larındadır.** Kısa ve net yazılır; yalnızca sıradaki adımların issue'ları açılır, ileri aşamalarınki zamanı gelince eklenir. Görev listesi depodaki dosyalara kopyalanmaz; depodaki "İlerleme" listesi kilometre taşı düzeyindedir.
3. **Tarihleri ve kararları gerekçesiyle yazın.** Örnek: takvim 15 Ocak'a uzatıldı (16 Kasım 2026), nedeni README §9.2'de.
4. **Atamayı ekip yapar.** Issue'ları ekip açar ve atar; agent'lar yalnızca kullanıcı istediğinde atama yapar, kendiliğinden kimseyi atamaz.
5. Geçersiz bilgi eklemeyin: iddialar README'deki dürüst raporlama ilkelerine uymalıdır (sonuçlar olumsuz olsa da olduğu gibi raporlanır, istatistiksel anlamlılık iddia edilmez).
6. Commit ve push yalnızca kullanıcı istediğinde yapılır.
7. Şemanın kaynağı `tools/baglanti-semasi/gen2.py`'dir; çalıştırınca `tools/baglanti-semasi/index.html` ve `docs/sema/index.html` yazılır (ikisi aynı olmalı). Şema değişince PDF de (`Suiz-Baglanti-Semasi.pdf`) `out/b1…b8.svg` dosyalarından yeniden üretilir.

## Güncel durum (28 Kasım 2026)

- 28 Kasım 2026: PR #9 (test altyapısı ve CI) ve PR #10 (sözleşme v1 komut kuralları) merge edildi. Görev takibi Notion'dan GitHub issue'larına taşındı: PR #9 ve #10 incelemesinden çıkan kararlar ve düzeltmeler #11–#18'de, Notion'daki açık görevler #20–#34'te (Faz 3 görevleri 7 Aralık civarında eklenir).

- 21 Kasım 2026: MOSFET kartları lehimlendi, elektrik bağlantıları kuruldu; 5 V adaptörün fişi kesilip klemensle bağlandı (gelen klemensli jak erkek çıktı). Henüz güç verilmedi, hiçbir test yapılmadı. Yataklar hazırlanıyor; ekim 19 Kasım'da yapılmadı, takvim 23 Kasım'da tek ekime göre yeniden kuruldu. Roka tohumu alındı.

- Robotistan siparişi ve 6 kapasitif nem sensörü (v2.0, HW-390, Robocombo) teslim alındı ve parçadan doğrulandı. Elde ayrıca dirençli tip sensörler var; deneyde kullanılmaz.
- Oje: kapasitif nem sensörleri toprağa girmeden önce kart kenarlarına şeffaf oje sürülür. Bu not şemada (her adımda, sensörlerin yanında) büyük kırmızı uyarı olarak durur. Kullanıcı 23 Kasım 2026'da sözlü hatırlatmanın bırakılmasını istedi; oturum sonlarında hatırlatmayın.
- MOSFET kartı (üç klemensli), akış sensörü, pompa ve şamandıra 16 Kasım'da parçalarla doğrulandı; şema ve dokümanlar düzeltildi (docs/donanim-plani.md §6.1).
- **Tek ekim (23 Kasım 2026 kararı; docs/yazilim-plani.md):** ekim en geç 30 Kasım; sensörler toprakta ve gerçek veri en geç 7 Aralık; kural tabanlı sulama iki yatakta ve E3 en geç 14 Aralık; kod dondurma 16 Aralık; A/B tam veri 17 Aralık – 5 Ocak (20 gün); hasat 6 Ocak; analiz ve yayın 7–10 Ocak; yayın dönemi 15 Ocak'ta biter. Gerekçe README §9.2.
- 17 Kasım 2026: Notion ana dokümanındaki proje bilgisi kaldırıldı (28 Kasım'da Notion tamamen bırakıldı). Test yatağı kabı (kasa) henüz alınmadı; ölçüleri netleşince alan ve litre hesapları gözden geçirilecek.
