# 🕷️ Crawlinger

**Crawlinger**, iç ağınızdaki web sitelerini tarayarak HTML sayfaları, stil dosyaları, scriptler, resimler ve dökümanlar gibi varlıkları keşfetmek ve kaydetmek için tasarlanmış basit bir Python tabanlı web tarayıcısıdır.

## ✨ Özellikler

- **Dahili Odaklı Tarama**: Yalnızca belirtilen başlangıç alan adı (domain) içerisindeki URL'leri takip eder.  
- **Varlık Keşfi**: HTML, CSS, JS, PDF, resimler ve daha fazlası gibi çeşitli varlık türlerini tanır.  
- **Ayarlanabilir Derinlik**: Tarayıcının ne kadar derine ineceğini kontrol etme imkânı sunar.  
- **JSON Çıktısı**: Keşfedilen tüm varlıkları, durum kodları ve diğer meta verilerle birlikte yapılandırılmış bir JSON dosyasına kaydeder.  
- **Gecikme Ayarı**: Sunucuya aşırı yük bindirmemek için HTTP istekleri arasına gecikme ekleme seçeneği sunar.

## 🚀 Kurulum

Bu betiği çalıştırmak için sisteminizde **Python 3** kurulu olmalıdır.

1. Projeyi klonlayın veya dosyaları indirin.
2. Gerekli Python kütüphanelerini `pip` kullanarak kurun:

```bash
pip install requests beautifulsoup4
```

## 💻 Kullanım

Crawlinger'ı komut satırından şu şekilde çalıştırabilirsiniz:

```bash
python crawlinger.py <başlangıç_url> [seçenekler]
```

### Argümanlar

- `start_url`: (Zorunlu) Taramanın başlayacağı tam URL. Örnek: `http://192.168.1.10`
- `--max_depth`: (İsteğe bağlı) Tarama derinliği. Varsayılan: `2`
- `--output_file`: (İsteğe bağlı) Sonuçların kaydedileceği JSON dosyası. Varsayılan: `discovered_web_assets.json`
- `--delay`: (İsteğe bağlı) İstekler arasındaki gecikme (saniye cinsinden). Varsayılan: `0.1`

### Örnek Komut

İç ağınızdaki `http://test-server.local` adresini 2 derinliğe kadar taramak ve sonuçları `test_server_assets.json` dosyasına kaydetmek için:

```bash
python crawlinger.py http://test-server.local --max_depth 2 --output_file test_server_assets.json
```

## 📄 Örnek Çıktı (`.json`)

Çıktı dosyası, keşfedilen her varlık için aşağıdaki gibi birer obje içeren bir JSON dizisi olacaktır:

```json
[
    {
        "url": "http://test-server.local/index.html",
        "type": "HTML",
        "status_code": 200,
        "content_type": "text/html; charset=utf-8",
        "size_bytes": 12345,
        "depth": 0
    },
    {
        "url": "http://test-server.local/styles/main.css",
        "type": "CSS",
        "status_code": 200,
        "content_type": "text/css",
        "size_bytes": 6789,
        "depth": 1,
        "source_url": "http://test-server.local/index.html"
    }
]
```

## ⚠️ Sorumluluk Reddi

**Crawlinger** yalnızca sahibi olduğunuz veya tarama izni açıkça verilmiş sistemlerde kullanılmalıdır. İzinsiz tarama yapmak, ağ politikalarını ihlal edebilir ve yasa dışı olabilir.
