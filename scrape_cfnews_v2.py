import requests
import re
import os
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.cfnews.net"
OUT_DIR = "scraped_cfnews"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

# Manual list from latest snapshot to ensure we get started
LINKS = [
    "/L-actualite/Capital-innovation/Operations/1er-tour/Games2gether-joue-avec-un-fonds-americain-595008",
    "/L-actualite/Capital-innovation/Operations/1er-tour/Homaio-emet-aupres-de-nouveaux-investisseurs-594998",
    "/L-actualite/International/Operations/M-A/RG-Group-se-ressource-aupres-d-un-industriel-allemand-595003",
    "/L-actualite/LBO/Operations/MBO/Kaviari-deguste-son-premier-MBO-595000",
    "/L-actualite/International/Operations/LBO/TheGuarantors-signe-un-bail-avec-un-new-yorkais-594963",
    "/L-actualite/Nominations/Fonds/Evercore-recrute-un-MD-594985",
    "/L-actualite/Nominations/Avocat/Sekri-Valentin-Zerrouk-coopte-594973",
    "/L-actualite/Build-up/Groupe-PG-s-electrise-593808",
    "/L-actualite/LBO/Operations/LBO-VI/Aserti-calibre-son-LBO-IV-593810"
]

def log(msg):
    print(f"CFNEWS: {msg}")

def scrape_article(url_path):
    url = BASE_URL + url_path
    name = url_path.split('/')[-1]
    path = f"{OUT_DIR}/{name}.md"
    if os.path.exists(path): return

    log(f"Scraping article: {url}")
    try:
        # CFNEWS might need a User-Agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # Extract main content
            content = soup.find('div', class_='article-content') or soup.find('article') or soup.body
            text = content.get_text(separator='\n', strip=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Article: {name}\n\nSource: {url}\n\n{text}")
        else:
            log(f"Failed {url}: {r.status_code}")
        time.sleep(2)
    except Exception as e:
        log(f"Error scraping {url}: {e}")

def main():
    log(f"Starting scrape of {len(LINKS)} specific articles.")
    for l in LINKS:
        scrape_article(l)
    log("Finished initial CFNEWS batch.")

if __name__ == "__main__":
    main()
