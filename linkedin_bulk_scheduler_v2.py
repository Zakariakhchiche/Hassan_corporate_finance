import asyncio
from playwright.async_api import async_playwright
import datetime
import sys
import re

def log(text):
    print(f"[{datetime.datetime.now()}] {text}")
    sys.stdout.flush()

def parse_posts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Correction du regex pour correspondre exactement au format du fichier
    parts = re.split(r'\n\d+\.\s+\*\*', content)
    posts = []
    
    current_date = datetime.date(2026, 2, 16)
    
    for i, part in enumerate(parts[1:], 1):
        if i > 30: break
        lines = part.strip().split('\n')
        title = lines[0].replace('**', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        while current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)
            
        posts.append({
            "text": f"{title}\n\n{body}",
            "iso_date": current_date.strftime("%Y-%m-%d"),
            "display_date": current_date.strftime("%d/%m/%Y"),
            "time": "09:00"
        })
        current_date += datetime.timedelta(days=1)
        
    return posts

async def schedule_post(page, post, index):
    log(f"--- Programming Post {index}/30 ({post['display_date']}) ---")
    try:
        await page.goto("https://www.linkedin.com/feed/")
        await asyncio.sleep(4)
        
        # Click Start Post
        await page.click("button.share-mb-launcher", timeout=15000)
        await asyncio.sleep(2)
        
        # Type content
        await page.fill("div[role='textbox']", post['text'])
        log("Text inserted.")
        await asyncio.sleep(1)
        
        # Click Schedule Icon
        # Try different selectors if aria-label fails
        log("Looking for schedule icon...")
        schedule_icon = page.locator("button[aria-label='Programmer pour plus tard']")
        if await schedule_icon.count() == 0:
            schedule_icon = page.locator(".share-promoted-detour-button") # Common class
        
        await schedule_icon.click(timeout=10000)
        log("Scheduler dialog opened.")
        await asyncio.sleep(2)
        
        # Fill Date & Time
        await page.fill("input[type='date']", post['iso_date'])
        await page.fill("input[type='time']", post['time'])
        log(f"Time set: {post['iso_date']} {post['time']}")
        await asyncio.sleep(1)
        
        # Click Next (Suivant)
        await page.click("button:has-text('Suivant')", timeout=5000)
        log("Clicked Suivant.")
        await asyncio.sleep(1)
        
        # Click Schedule (Programmer)
        await page.click("button:has-text('Programmer')", timeout=5000)
        log("Final Schedule button clicked.")
        
        # Wait for confirmation
        await asyncio.sleep(4)
        log(f"Post {index} success.")
        return True
    except Exception as e:
        log(f"Post {index} failed: {e}")
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)
        await page.keyboard.press("Escape")
        return False

async def main():
    posts = parse_posts("tous_les_posts_linkedin.md")
    log(f"Ready to deploy {len(posts)} posts.")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            for i, post in enumerate(posts, 1):
                success = await schedule_post(page, post, i)
                if not success:
                    log("Aborting to let user check the browser.")
                    break
                await asyncio.sleep(2)
                
            await browser.close()
        except Exception as e:
            log(f"Global error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
