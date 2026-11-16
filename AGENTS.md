# AGENTS.md — Suİz depo kuralları (insanlar ve AI agent'lar için)

Bu depo ile **Notion** senkron tutulur. Önce bunu okuyun, sonra düzenleme yapın.

## İki kaynak, tek bilgi

| Kaynak | Rolü |
| :--- | :--- |
| **Notion — "Suİz — Proje Genel Yapısı" sayfası** (ana doküman) | Proje bilgisinin canlı hali: mimari, takvim, kararlar, donanım, açık noktalar |
| **Notion — "Görevler" tahtası** (ana dokümanın en altında) | Görev durumunun tek kaynağı (Yapılacak / Yapılıyor / Yapıldı). Görevler bu depoya kopyalanmaz |
| **Bu depo (GitHub: [Berceste-Team/Su-z](https://github.com/Berceste-Team/Su-z))** | Yayınlanacak teknik kayıt: `README.md` (proje şartnamesi) ve `docs/donanim-plani.md` (donanım ve tesisat). Kod `firmware/`, `app/`, `simulation/` altına gelecek |

Notion'daki ana doküman ile `README.md` + `docs/donanim-plani.md` aynı karar ve tarihleri içermelidir.

## Kurallar

1. **Bir karar, takvim, donanım ya da deney değişikliği iki yerde de yapılır.** Birini düzenleyen, diğerini de aynı iş içinde günceller; yapamıyorsa farkı kullanıcıya bildirir. Çelişki fark ederseniz sessizce birini seçmeyin, kullanıcıya sorun.
2. **Görev durumu yalnızca Notion tahtasındadır.** Depodaki "İlerleme" listesi kilometre taşı düzeyindedir.
3. **Tarihleri ve kararları gerekçesiyle yazın.** Örnek: takvim 15 Ocak'a uzatıldı (16 Kasım 2026), nedeni README §9.2'de.
4. Sorumlu alanı Notion'da bilerek boştur; ekip kendisi seçer, atama yapmayın.
5. Geçersiz bilgi eklemeyin: iddialar README'deki dürüst raporlama ilkelerine uymalıdır (sonuçlar olumsuz olsa da olduğu gibi raporlanır, istatistiksel anlamlılık iddia edilmez).
6. Commit ve push yalnızca kullanıcı istediğinde yapılır.

## Güncel durum (16 Kasım 2026)

- Robotistan siparişi ve 6 kapasitif nem sensörü (v2.0, HW-390) teslim alındı ve parçadan doğrulandı. Elde ayrıca dirençli tip sensörler var; deneyde kullanılmaz.
- **Kullanıcıya hatırlat (kendisi istedi, 16 Kasım 2026):** kapasitif nem sensörleri toprağa girmeden önce kart kenarlarına şeffaf oje sürülmeli, elektronik kısım oje ya da makaronla korunmalı. Bu iş yapıldığı teyit edilene kadar, sensörler ya da ekim konuşulduğunda ve her oturumun sonunda hatırlatın; yapılınca bu maddeyi silin.
- MOSFET kartı (üç klemensli), akış sensörü, pompa ve şamandıra 16 Kasım'da parçalarla doğrulandı; şema ve dokümanlar düzeltildi (docs/donanim-plani.md §6.1). Şemanın kaynağı `tools/baglanti-semasi/gen2.py`; çalıştırınca `docs/sema/index.html` de yazılır.
- **İki tur korunur; takvim 15 Ocak 2027'de biter.** Tur 1: 19 Kasım – 13 Aralık (sensörler toprakta 24 Kasım; kural tabanlı sulama Yatak B 3 Aralık, Yatak A 8 Aralık; güvenlik testleri 9–11 Aralık); kod ve donanım 13 Aralık'ta donar; Tur 2 / E5 A/B deneyi 14 Aralık – 7 Ocak; analiz ve yayın 8–10 Ocak.
- Notion ana dokümanında en güncel hal bulunur; farklılık varsa Notion'a göre depoyu güncelleyin ve bunu kullanıcıya söyleyin.
