import requests
import re
import os
import time

BASE_URL = "https://annuairecorporatefinance.fr/entreprises/"
OUT_DIR = "scraped_annuaire"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def log(msg):
    with open("scrape.log", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()}: {msg}\n")
    print(msg)

def get_links():
    all_links = set()
    for p in range(1, 23):
        url = f"{BASE_URL}page/{p}/" if p > 1 else BASE_URL
        log(f"Fetching links from page {p}...")
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # Extract links like https://annuairecorporatefinance.fr/entreprises/name/
                found = re.findall(r'https://annuairecorporatefinance\.fr/entreprises/[^/"]+/', r.text)
                for f in found:
                    if f != BASE_URL and "/page/" not in f:
                        all_links.add(f)
            time.sleep(1)
        except Exception as e:
            log(f"Error on page {p}: {e}")
    return list(all_links)

def scrape_page(url):
    name = url.strip('/').split('/')[-1]
    path = f"{OUT_DIR}/{name}.md"
    if os.path.exists(path):
        return
    
    log(f"Scraping {url}...")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # Simple text extraction for now
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.content, 'html.parser')
            # Look for main content (usually article or main)
            main = soup.find('main') or soup.find('article') or soup.body
            text = main.get_text(separator='\n', strip=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {name}\n\nSource: {url}\n\n{text}")
        time.sleep(1)
    except Exception as e:
        log(f"Error on {url}: {e}")

def main():
    links = get_links()
    log(f"Found {len(links)} unique company links.")
    for l in links:
        scrape_page(l)

if __name__ == "__main__":
    main()
