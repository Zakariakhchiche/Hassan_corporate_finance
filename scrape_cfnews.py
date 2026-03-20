import requests
import re
import os
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.cfnews.net"
OUT_DIR = "scraped_cfnews"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def log(msg):
    print(f"CFNEWS: {msg}")

def get_news_links():
    url = f"{BASE_URL}/L-actualite"
    log(f"Fetching news: {url}")
    links = set()
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # Extract links with pattern /L-actualite/...-595008 (id at end)
            found = re.findall(r'/L-actualite/[^"]+-\d+', r.text)
            for f in found:
                links.add(BASE_URL + f)
        return list(links)
    except Exception as e:
        log(f"Error fetching news list: {e}")
        return []

def scrape_article(url):
    name = url.split('/')[-1]
    path = f"{OUT_DIR}/{name}.md"
    if os.path.exists(path): return

    log(f"Scraping article: {url}")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            # Look for article content
            content = soup.find('div', class_='article-content') or soup.find('article') or soup.body
            text = content.get_text(separator='\n', strip=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Article: {name}\n\nSource: {url}\n\n{text}")
        time.sleep(1)
    except Exception as e:
        log(f"Error scraping {url}: {e}")

def main():
    links = get_news_links()
    log(f"Found {len(links)} current articles.")
    for l in links:
        scrape_article(l)

if __name__ == "__main__":
    main()
