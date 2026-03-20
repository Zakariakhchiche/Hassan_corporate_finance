import requests
import re
import os
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.fusacq.com/"
OUT_DIR = "scraped_fusacq"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

CATEGORIES = [
    "annuaire-des-experts/a2260,reprise-cession-creation-franchise_fr_",
    "annuaire-des-experts/a2258,comptabilite-audit-financement-assurance_fr_",
    "annuaire-des-experts/a2259,droit_fiscalite_patrimoine_immobilier_fr_",
    "annuaire-des-experts/a2257,informatique-bureautique-telecom_fr_",
    "annuaire-des-experts/a2256,marketing-vente_fr_",
    "annuaire-des-experts/a2261,ressources-humaines_fr_"
]

def log(msg):
    print(f"FUSACQ: {msg}")

def get_links(cat_url):
    url = f"{BASE_URL}{cat_url}"
    log(f"Fetching category: {url}")
    links = set()
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # Extract links to specific expert profiles or sub-activities
            # In the expert directory, links usually contain 'activite-'
            found = re.findall(r'href="/(activite-[^"]+)"', r.text)
            for f in found:
                links.add(BASE_URL + f)
        return list(links)
    except Exception as e:
        log(f"Error on {cat_url}: {e}")
        return []

def scrape_expert(url):
    name = url.split(',')[-1].replace('_fr_', '').strip('/')
    path = f"{OUT_DIR}/{name}.md"
    if os.path.exists(path): return

    log(f"Scraping expert: {url}")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            content = soup.find('main') or soup.find('article') or soup.body
            text = content.get_text(separator='\n', strip=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Expert: {name}\n\nSource: {url}\n\n{text}")
        time.sleep(0.5)
    except Exception as e:
        log(f"Error scraping {url}: {e}")

def main():
    all_links = []
    for cat in CATEGORIES:
        links = get_links(cat)
        all_links.extend(links)
    
    all_links = list(set(all_links))
    log(f"Found {len(all_links)} total expert links.")
    for l in all_links:
        scrape_expert(l)

if __name__ == "__main__":
    main()
