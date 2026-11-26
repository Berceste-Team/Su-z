# CLAUDE.md — Suİz

## Bilgi kaynakları
- Repo kuralları: [AGENTS.md](AGENTS.md). Yazılım tasarımı (veri yolu, sözleşme, klasörler):
  [docs/yazilim-plani.md](docs/yazilim-plani.md).
- Öncelik: proje sitesi (`docs/index.html`) > README.md > docs/yazilim-plani.md.
- Tarih, takvim, durum ve projenin hangi aşamada olduğu bu dosyada tutulmaz; her işten
  önce siteden okunur.
- Bir bilgi hiçbir kaynakta yoksa varsayım yapılmaz: değer ayar olarak bırakılır ve
  kullanıcıya sorulur. Kaynaklar çelişirse sessizce biri seçilmez, kullanıcıya sorulur.

## Kapsam
Bu repodaki Python kodu UNO Q'nun Linux tarafında çalışır: veriyi alır, kaydeder,
kontrol eder, karar verir ve panoda gösterir. MCU sketch'i donanım tarafınındır.
İki taraf yalnızca veri sözleşmesindeki `suiz_*` mesajlarıyla konuşur; mesaj adları,
alanlar ve kodlar `app/ingest/contract.py`'de tek yerde tutulur. Sözleşme değişikliği
önce belgeye, sonra koda işlenir.

## Değişmez kurallar
- TDD: önce başarısız test, sonra geçiren en küçük kod, sonra düzenleme.
- Commit ve push yalnızca kullanıcı isteyince yapılır. Her iş main'den açılan kısa
  ömürlü dalda (`feature/…`, `fix/…`, `docs/…`) yapılır ve PR ile main'e girer.
- Testler kart olmadan, sahte (mock) veriyle ve sahte Bridge ile çalışır; kartta
  işletme gerçek veriyle yapılır. Her kayıt `is_synthetic` taşır; sentetik veri
  hiçbir analize, rapora ya da karara gerçek veri gibi girmez.
- Bridge (`arduino.app_utils`) yalnızca `app/ingest/bridge_adapter.py` ve `app/control/`
  içinde import edilir; geri kalan her modül kartsız çalışabilmelidir.
- Python pompayı doğrudan açmaz, MCU'ya yalnızca istek gönderir. Güvenlik kuralları
  MCU'dadır; Python'daki kontroller ek katmandır, onların yerine geçmez.
- Bütçe ve doz mm cinsindedir (1 mm = 1 L/m²). Yatak alanı, eşikler, saatler ve
  limitler koda gömülmez, ayar dosyalarından okunur.
- Saklanan zaman damgaları UTC'dir ve saat dilimi bilgisi taşır.
- Kod dondurulduktan sonra yalnızca güvenlik düzeltmesi yapılır (dondurma durumu
  siteden okunur).

## Kod üslubu
- Tip ipuçları; değer nesneleri için `@dataclass(frozen=True)` veya `NamedTuple`;
  hatalı girdi `ValueError` ile reddedilir.
- Kod, docstring ve commit mesajları İngilizce; belgeler Türkçe.
- Önce standart kütüphane; yeni bağımlılık gerekçesiyle `requirements.txt`'e eklenir.
- Testler deterministiktir: sahte veri sabit seed ile üretilir.

## Komutlar (Windows, PowerShell)
- Ortam: `python -m venv .venv`, `.venv\Scripts\activate`, `pip install -r requirements-dev.txt`
- Test: `python -m pytest`
- CI: her PR'da `.github/workflows/tests.yml` çalışır.

## Bitti tanımı
Bir görev, [docs/yazilim-plani.md](docs/yazilim-plani.md) §9'daki koşulların hepsi
sağlanınca bitmiş sayılır:
- Kod main'e merge edildi ve CI yeşil.
- Yeni davranışın testi var (mock veriyle çalışması yeterli).
- Notion görevindeki kabul kriterleri, incelemeyi yapan kişi tarafından kontrol edildi.
- Bir veri alanı ya da mesaj değiştiyse `docs/data-contract.md` güncellendi (dosya
  main'e girene kadar sözleşme yazılım planı §4'tedir).
