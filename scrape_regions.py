import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://www.fusacq.com/annuaire-des-experts/a3296,experts-specialises-en-cession-d-entreprise,33_{:02d},{}-france_fr_"
OUT_DIR = "scraped_fusacq_regions"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

REGIONS = [
    (1, "alsace"), (2, "aquitaine"), (3, "auvergne"), (4, "basse-normandie"),
    (5, "bourgogne"), (6, "bretagne"), (7, "centre"), (8, "champagne-ardenne"),
    (9, "corse"), (10, "franche-comte"), (11, "haute-normandie"), (12, "ile-de-france"),
    (13, "languedoc-roussillon"), (14, "limousin"), (15, "lorraine"), (16, "midi-pyrenees"),
    (17, "nord-pas-de-calais"), (18, "pays-de-la-loire"), (19, "picardie"), (20, "poitou-charentes"),
    (21, "provence-alpes-cote-d-azur"), (22, "rhone-alpes"), (23, "dom-tom")
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def log(msg):
    with open("scrape_regions.log", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()}: {msg}\n")
    print(msg)

def scrape_region(idx, name):
    url = BASE_URL.format(idx, name)
    log(f"Scraping region {name} (ID {idx:02d})...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # Each expert is usually in a div or generic container
            # In the snapshot, experts are in generic containers with link, heading, description
            # Let's find the main content area
            container = soup.find('div', id='cadre_principal') or soup.find('main') or soup.body
            
            # Simple text extraction for the whole region for now (faster for RAG)
            text = container.get_text(separator='\n', strip=True)
            
            with open(f"{OUT_DIR}/{name}.md", "w", encoding="utf-8") as f:
                f.write(f"# Experts - Region: {name.upper()}\n")
                f.write(f"Source: {url}\n\n")
                f.write(text)
            log(f"Saved region {name}.")
        else:
            log(f"Failed {name}: {r.status_code}")
        time.sleep(2)
    except Exception as e:
        log(f"Error on {name}: {e}")

def main():
    log("Starting bulk regional scrape...")
    for idx, name in REGIONS:
        scrape_region(idx, name)
    log("Finished regional scrape.")

if __name__ == "__main__":
    main()
