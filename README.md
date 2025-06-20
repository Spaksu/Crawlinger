# 🕷️ Crawlinger

Crawlinger, iç ağınızdaki web sitelerini tarayarak HTML sayfaları, stil dosyaları, scriptler, resimler ve dökümanlar gibi varlıkları keşfetmek ve kaydetmek için tasarlanmış basit bir Python tabanlı web tarayıcısıdır.

## ✨ Özellikler

-   **Dahili Odaklı Tarama**: Yalnızca belirtilen başlangıç alan adı (domain) içerisindeki URL'leri takip eder.
-   **Varlık Keşfi**: HTML, CSS, JS, PDF, resimler ve daha fazlası gibi çeşitli varlık türlerini tanır.
-   **Ayarlanabilir Derinlik**: Tarayıcının ne kadar derine ineceğini kontrol etme imkanı sunar.
-   **JSON Çıktısı**: Keşfedilen tüm varlıkları, durum kodları ve diğer meta verilerle birlikte yapılandırılmış bir JSON dosyasına kaydeder.
-   **Gecikme Ayarı**: Sunucuya aşırı yük bindirmemek için HTTP istekleri arasına gecikme ekleme seçeneği sunar.

## 🚀 Kurulum

Bu betiği çalıştırmak için sisteminizde **Python 3**'ün kurulu olması gerekmektedir.

1.  Projeyi klonlayın veya dosyaları indirin.

2.  Gerekli Python kütüphanelerini `pip` kullanarak kurun:

    \`\`\`bash
    pip install requests beautifulsoup4
    \`\`\`

## 💻 Kullanım

Crawlinger'ı komut satırından çalıştırabilirsiniz. Temel kullanım aşağıdaki gibidir:

\`\`\`bash
python scripts/crawlinger.py <başlangıç_url> [seçenekler]
\`\`\`

### Argümanlar

-   `start_url`: (Zorunlu) Taramanın başlayacağı tam URL. Örn: `http://192.168.1.10`
-   `--max_depth`: (İsteğe bağlı) Tarama derinliği. Varsayılan değer: `2`.
-   `--output_file`: (İsteğe bağlı) Sonuçların kaydedileceği JSON dosyasının adı. Varsayılan değer: `discovered_web_assets.json`.
-   `--delay`: (İsteğe bağlı) İstekler arasındaki saniye cinsinden gecikme. Varsayılan değer: `0.1`.

### Örnek Komut

İç ağınızdaki `http://test-server.local` adresini 2 derinliğe kadar taramak ve sonuçları `test_server_assets.json` dosyasına kaydetmek için:

\`\`\`bash
python scripts/crawlinger.py http://test-server.local --max_depth 2 --output_file test_server_assets.json
\`\`\`

## 📄 Örnek Çıktı (`.json`)

Çıktı dosyası, keşfedilen her varlık için bir obje içeren bir JSON dizisi olacaktır:

\`\`\`json
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
\`\`\`

## ⚠️ Sorumluluk Reddi

Bu aracı yalnızca sahibi olduğunuz veya tarama yapmak için açıkça izniniz olan ağlarda ve sistemlerde kullanın. İzinsiz tarama yapmak, ağ politikalarını ihlal edebilir ve yasa dışı olabilir.
