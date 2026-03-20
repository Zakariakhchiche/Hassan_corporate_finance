import requests
import re
import os
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.fusacq.com/"
OUT_DIR = "scraped_fusacq"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def log(msg):
    print(f"FUSACQ: {msg}")

def get_expert_links():
    url = f"{BASE_URL}annuaire_experts_fr_"
    log(f"Fetching experts directory: {url}")
    links = set()
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # Look for expert profile links. Usually they have specific patterns.
            # From snapshot, activities look like /activite-2209,conseil-m-a_fr_
            # Let's find links containing 'activite-'
            for a in soup.find_all('a', href=True):
                href = a['href']
                if "activite-" in href:
                    links.add(BASE_URL + href.lstrip('/'))
        return list(links)
    except Exception as e:
        log(f"Error fetching directory: {e}")
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
            main = soup.find('main') or soup.find('article') or soup.body
            text = main.get_text(separator='\n', strip=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Expert: {name}\n\nSource: {url}\n\n{text}")
        time.sleep(1)
    except Exception as e:
        log(f"Error scraping {url}: {e}")

def main():
    links = get_expert_links()
    log(f"Found {len(links)} activities/experts categories.")
    for l in links:
        scrape_expert(l)

if __name__ == "__main__":
    main()
