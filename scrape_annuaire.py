import requests
from bs4 import BeautifulSoup
import time
import os

BASE_URL = "https://annuairecorporatefinance.fr/entreprises/"
OUT_DIR = "scraped_annuaire"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def get_company_links(page_num):
    url = f"{BASE_URL}page/{page_num}/" if page_num > 1 else BASE_URL
    print(f"Fetching page {page_num}...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Based on the structure observed in web_fetch, links to detail pages are in the company titles
        # In the markdown they look like: [21 INVEST](https://annuairecorporatefinance.fr/entreprises/21-invest-france/)
        # Usually they are inside h3 or similar. Let's look for links starting with the base detail path.
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "/entreprises/" in href and href != BASE_URL and not "/page/" in href:
                # Clean up and avoid duplicates
                links.append(href)
        
        return list(set(links))
    except Exception as e:
        print(f"Exception on page {page_num}: {e}")
        return []

def scrape_detail(url):
    print(f"Scraping detail: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Get content - usually a specific container
        content = soup.get_text(separator='\n')
        
        name = url.strip('/').split('/')[-1]
        with open(f"{OUT_DIR}/{name}.txt", "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\n\n")
            f.write(content)
        return name
    except Exception as e:
        print(f"Exception on {url}: {e}")
        return None

def main():
    all_links = []
    # Test with first 2 pages first to see if it works
    for i in range(1, 23):
        links = get_company_links(i)
        all_links.extend(links)
        time.sleep(1) # Be respectful
    
    all_links = list(set(all_links))
    print(f"Found {len(all_links)} company links.")
    
    for link in all_links:
        scrape_detail(link)
        time.sleep(1)

if __name__ == "__main__":
    main()
