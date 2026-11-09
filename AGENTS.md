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
3. **Tarihleri ve kararları gerekçesiyle yazın.** Örnek: Tur 1 kısaltıldı (15 Kasım – 3 Aralık, 9 Kasım 2026), nedeni README §9.2'de.
4. Sorumlu alanı Notion'da bilerek boştur; ekip kendisi seçer, atama yapmayın.
5. Geçersiz bilgi eklemeyin: iddialar README'deki dürüst raporlama ilkelerine uymalıdır (sonuçlar olumsuz olsa da olduğu gibi raporlanır, istatistiksel anlamlılık iddia edilmez).
6. Commit ve push yalnızca kullanıcı istediğinde yapılır.

## Güncel durum (9 Kasım 2026)

- Robotistan siparişi teslim alındı; kapasitif sensörler (direnc.net, 6 adet) henüz sipariş edilmedi.
- **İki tur korunur.** Tur 1 ekimi 15 Kasım – 3 Aralık (kural tabanlı sulama, model ≈ 28 Kasım'dan itibaren gölge modda, E2 kuruma eğrileri 19 Kasım – 3 Aralık); kod ve donanım 3 Aralık'ta donar; Tur 2 / E5 A/B deneyi 4–27 Aralık; yayın 30 Aralık.
- Notion ana dokümanında en güncel hal bulunur; farklılık varsa Notion'a göre depoyu güncelleyin ve bunu kullanıcıya söyleyin.
