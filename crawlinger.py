import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import json
import time

# Tanımlanmış varlık türleri ve uzantıları
ASSET_EXTENSIONS = {
    '.html': 'HTML', '.htm': 'HTML',
    '.css': 'CSS',
    '.js': 'JavaScript',
    '.json': 'JSON Data',
    '.xml': 'XML Data',
    '.txt': 'Text File',
    '.pdf': 'PDF Document',
    '.doc': 'Word Document', '.docx': 'Word Document',
    '.xls': 'Excel Spreadsheet', '.xlsx': 'Excel Spreadsheet',
    '.ppt': 'PowerPoint Presentation', '.pptx': 'PowerPoint Presentation',
    '.jpg': 'JPEG Image', '.jpeg': 'JPEG Image',
    '.png': 'PNG Image',
    '.gif': 'GIF Image',
    '.svg': 'SVG Image',
    '.webp': 'WebP Image',
    '.ico': 'Icon File',
    '.mp4': 'MP4 Video', '.webm': 'WebM Video',
    '.mp3': 'MP3 Audio', '.wav': 'WAV Audio',
}

# HTTP istekleri için kullanıcı aracısı (User-Agent)
HEADERS = {
    'User-Agent': 'Crawlinger/1.0 (https://vercel.com/v0)'
}

def get_asset_type(url):
    """URL'den dosya uzantısına göre varlık türünü belirler."""
    parsed_url = urlparse(url)
    path = parsed_url.path
    for ext, asset_type in ASSET_EXTENSIONS.items():
        if path.lower().endswith(ext):
            return asset_type
    if not any(path.lower().endswith(ext_group) for ext_group in ['.css', '.js', '.json', '.xml', '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.mp4', '.webm', '.mp3', '.wav']):
        return 'Web Page (HTML or other)'
    return 'Unknown'

def is_internal(url, base_domain):
    """URL'nin başlangıç domain'i ile aynı domain'de olup olmadığını kontrol eder."""
    parsed_url = urlparse(url)
    return parsed_url.netloc == base_domain

def crawl_website(start_url, max_depth=2, delay_between_requests=0.1):
    """
    Belirtilen URL'den başlayarak web sitesini tarar ve varlıkları toplar.
    """
    if not (start_url.startswith('http://') or start_url.startswith('https://')):
        print(f"Hata: Geçersiz başlangıç URL'si '{start_url}'. 'http://' veya 'https://' ile başlamalıdır.")
        return []

    base_domain = urlparse(start_url).netloc
    urls_to_visit = [(start_url, 0)]  # (url, depth)
    visited_urls = set()
    discovered_assets = []

    print(f"Crawlinger starting from: {start_url} (Max Depth: {max_depth})")
    print(f"Targeting base domain: {base_domain}")

    while urls_to_visit:
        current_url, depth = urls_to_visit.pop(0)

        if current_url in visited_urls or depth > max_depth:
            continue

        visited_urls.add(current_url)
        print(f"Visiting [Depth {depth}]: {current_url}")

        try:
            response = requests.get(current_url, headers=HEADERS, timeout=10, allow_redirects=True)
            effective_url = response.url
            
            if urlparse(effective_url).netloc != base_domain:
                print(f"  Skipping (redirected to external domain): {effective_url}")
                asset_info = {
                    "url": effective_url,
                    "type": "External Redirect",
                    "status_code": response.status_code,
                    "depth": depth,
                    "source_url": current_url
                }
                discovered_assets.append(asset_info)
                continue

            asset_type = get_asset_type(effective_url)
            if response.headers.get('Content-Type') and 'text/html' in response.headers['Content-Type'].lower() and asset_type == 'Unknown':
                 asset_type = 'HTML Page'

            asset_info = {
                "url": effective_url,
                "type": asset_type,
                "status_code": response.status_code,
                "content_type": response.headers.get('Content-Type', 'N/A'),
                "size_bytes": len(response.content),
                "depth": depth
            }
            discovered_assets.append(asset_info)
            print(f"  Discovered: {asset_type} (Status: {response.status_code})")

            if response.status_code == 200 and \
               response.headers.get('Content-Type') and \
               'text/html' in response.headers['Content-Type'].lower() and \
               depth &lt; max_depth:
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(effective_url, href)
                    parsed_absolute_url = urlparse(absolute_url)
                    clean_url = parsed_absolute_url._replace(fragment='').geturl()

                    if is_internal(clean_url, base_domain) and clean_url not in visited_urls:
                        urls_to_visit.append((clean_url, depth + 1))
                
                for tag_name, attr_name in [('img', 'src'), ('link', 'href'), ('script', 'src')]:
                    for tag in soup.find_all(tag_name, **{attr_name: True}):
                        asset_url_relative = tag[attr_name]
                        asset_url_absolute = urljoin(effective_url, asset_url_relative)
                        parsed_asset_url = urlparse(asset_url_absolute)
                        clean_asset_url = parsed_asset_url._replace(fragment='').geturl()

                        if is_internal(clean_asset_url, base_domain) and clean_asset_url not in visited_urls and clean_asset_url not in [a['url'] for a in discovered_assets]:
                            asset_response_head = requests.head(clean_asset_url, headers=HEADERS, timeout=5, allow_redirects=True)
                            asset_type_linked = get_asset_type(clean_asset_url)
                            if asset_response_head.headers.get('Content-Type') and 'text/html' in asset_response_head.headers['Content-Type'].lower() and asset_type_linked == 'Unknown':
                                asset_type_linked = 'HTML Page (Linked)'

                            linked_asset_info = {
                                "url": clean_asset_url,
                                "type": asset_type_linked,
                                "status_code": asset_response_head.status_code,
                                "content_type": asset_response_head.headers.get('Content-Type', 'N/A'),
                                "size_bytes": int(asset_response_head.headers.get('Content-Length', 0)),
                                "depth": depth + 1,
                                "source_url": effective_url
                            }
                            if clean_asset_url not in [da['url'] for da in discovered_assets]:
                                discovered_assets.append(linked_asset_info)
                                print(f"  Found linked asset: {clean_asset_url} ({asset_type_linked})")
                            if asset_type_linked.startswith('HTML') and clean_asset_url not in visited_urls:
                                urls_to_visit.append((clean_asset_url, depth + 1))

        except requests.exceptions.RequestException as e:
            print(f"  Error visiting {current_url}: {e}")
            asset_info = {
                "url": current_url,
                "type": "Error",
                "status_code": "N/A",
                "error_message": str(e),
                "depth": depth
            }
            discovered_assets.append(asset_info)
        
        time.sleep(delay_between_requests)

    return discovered_assets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawlinger: A simple web crawler for internal assets.")
    parser.add_argument("start_url", type=str, help="The starting URL to crawl (e.g., http://localhost:8000).")
    parser.add_argument("--max_depth", type=int, default=2, help="Maximum depth to crawl. Default is 2.")
    parser.add_argument("--output_file", type=str, default="discovered_web_assets.json", help="File to save the discovered assets (JSON format). Default is discovered_web_assets.json.")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay in seconds between requests. Default is 0.1s.")

    args = parser.parse_args()

    crawled_data = crawl_website(args.start_url, args.max_depth, args.delay)

    if crawled_data:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(crawled_data, f, indent=4, ensure_ascii=False)
        print(f"\nCrawling finished. {len(crawled_data)} assets/pages discovered.")
        print(f"Results saved to {args.output_file}")
    else:
        print("\nNo assets discovered or an error occurred.")
