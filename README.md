# Doğal Dil Tabanlı Gereksinim Metinlerinin Analizi ve Kalite Değerlendirmesi

Bu proje, doğal dilde yazılmış gereksinim metinlerini analiz eden ve kalite değerlendirmesi yapan web tabanlı bir uygulamadır.

## Özellikler

- Gereksinim metinlerini cümlelere ayırma
- Functional Requirement / Non-Functional Requirement sınıflandırması
- Muğlak ifade tespiti
- Kalite değerlendirmesi
- İyileştirme önerisi sunma
- Basit ve kullanıcı dostu web arayüzü

## Kullanılan Teknolojiler

- Python
- FastAPI
- Jinja2
- HTML
- CSS

## Gereksinimler

Başlamadan önce bilgisayarında **Python 3.10 veya üzeri** kurulu olmalıdır. Kurulu olup olmadığını kontrol etmek için bir terminal (komut satırı) açıp şunu yaz:

```bash
python3 --version
```

Eğer `Python 3.x.x` gibi bir çıktı görüyorsan kuruludur. "command not found" benzeri bir hata alırsan Python'ı https://www.python.org/downloads/ adresinden indirip kurmalısın.

> Not: macOS ve Linux'ta komut genelde `python3`, Windows'ta ise `python`'dur. Aşağıdaki adımlarda macOS/Linux için `python3`, Windows için `python` kullan.

## Kurulum

Projeyi bilgisayarına almak için iki yöntemden **birini** seçebilirsin.

### Yöntem 1 — Git ile klonlama (önerilen)

Bilgisayarında Git kuruluysa, bir terminal açıp projeyi indirmek istediğin klasöre git (örneğin Masaüstü) ve şu komutları çalıştır:

```bash
cd Desktop
git clone https://github.com/melistura/requirements-quality-analyzer.git
cd requirements-quality-analyzer
```

Artık proje klasörünün içindesin.

### Yöntem 2 — ZIP olarak indirme

Git kullanmak istemiyorsan:

1. Bu sayfanın üst kısmındaki yeşil **Code** butonuna tıkla.
2. Açılan menüden **Download ZIP** seçeneğine tıkla.
3. İnen `requirements-quality-analyzer-main.zip` dosyasını çift tıklayıp çıkar (klasör genelde `requirements-quality-analyzer-main` adıyla oluşur).
4. Bir terminal açıp bu klasörün içine gir. Örneğin Masaüstü'ne çıkardıysan:

```bash
cd Desktop/requirements-quality-analyzer-main
```

> Önemli: İndirdiğin klasörün içindeki `.py` dosyalarına (main.py, analyzer.py gibi) **çift tıklayarak çalıştırmaya çalışma**. Bu bir web uygulaması; aşağıdaki adımlarla terminalden başlatılır.

## Sanal Ortam Oluşturma

Proje klasörünün içindeyken, bağımlılıkların sistemi kirletmemesi için bir sanal ortam oluştur ve etkinleştir:

```bash
python3 -m venv .venv
```

Ardından etkinleştir:

```bash
# macOS / Linux:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

Etkinleştirme başarılıysa, terminal satırının başında `(.venv)` yazısını görürsün.

## Bağımlılıkları Yükleme

`(.venv)` aktifken, projenin ihtiyaç duyduğu kütüphaneleri yükle:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Uygulamayı başlatmak için:

```bash
uvicorn app.main:app --reload
```

Terminalde aşağıdakine benzer bir satır görürsün:

```
Uvicorn running on http://127.0.0.1:8000
```

## Kullanım

1. Bir web tarayıcısı aç (Chrome, Safari vb.).
2. Adres çubuğuna şunu yaz ve git: **http://127.0.0.1:8000**
3. Açılan ekranda metin kutusuna her satıra bir gereksinim yazıp **Analiz Et** butonuna bas.
4. Sistem her gereksinimi sınıflandırır, muğlak ifadeleri tespit eder, kalite değerlendirmesi yapar ve özet bir sonuç paneli gösterir.

## Uygulamayı Durdurma

Terminalde **Ctrl + C** tuşlarına basarak sunucuyu durdurabilirsin. Sanal ortamdan çıkmak için ise `deactivate` yazman yeterlidir.

## Proje Yapısı

```
requirements-quality-analyzer/
├── app/
│   ├── main.py          # FastAPI uygulaması ve uç noktalar
│   ├── analyzer.py      # Analiz, sınıflandırma ve kalite değerlendirme mantığı
│   ├── templates/
│   │   └── index.html   # Kullanıcı arayüzü şablonu
│   └── static/
│       └── style.css    # Stil dosyası
├── requirements.txt
├── README.md
└── .gitignore
```

## Sık Karşılaşılan Hatalar

- **`command not found: python`** → `python` yerine `python3` kullan.
- **`pip: command not found`** → `pip` yerine `pip3` ya da `python3 -m pip install -r requirements.txt` dene.
- **`uvicorn: command not found`** → Sanal ortamın etkin (`(.venv)`) olduğundan ve `pip install -r requirements.txt` adımını çalıştırdığından emin ol.
- **Adres açılmıyor** → Terminalde sunucunun çalıştığından ve adresi `http://127.0.0.1:8000` olarak doğru yazdığından emin ol.