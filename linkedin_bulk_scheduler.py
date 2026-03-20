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
    
    # Split by numbers followed by a dot (e.g., "1. ")
    parts = re.split(r'\n\d+\.\s+\*\*', content)
    posts = []
    
    # Start date: Monday Feb 16, 2026
    current_date = datetime.date(2026, 2, 16)
    
    for i, part in enumerate(parts[1:], 1):
        if i > 30: break
        
        # Extract title and body
        lines = part.strip().split('\n')
        title = lines[0].replace('**', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        # Remove hashtags from the end to put them later if needed, or keep them
        # For now, keep as is.
        
        # Skip weekends for scheduling (optional, but requested at 09:00, usually business days)
        while current_date.weekday() >= 5: # 5=Sat, 6=Sun
            current_date += datetime.timedelta(days=1)
            
        posts.append({
            "text": f"{title}\n\n{body}",
            "date": current_date.strftime("%d/%m/%Y"),
            "iso_date": current_date.strftime("%Y-%m-%d"),
            "time": "09:00"
        })
        current_date += datetime.timedelta(days=1)
        
    return posts

async def schedule_post(page, post, index):
    log(f"Starting post {index}: {post['date']}")
    try:
        # Reload to clear state
        await page.goto("https://www.linkedin.com/feed/")
        await asyncio.sleep(5)
        
        # Click Start Post
        # Use a more generic but robust selector
        log("Searching for 'Commencer un post' button...")
        start_button = page.get_by_role("button", name="Commencer un post", exact=True)
        if await start_button.count() == 0:
             # Try other variant
             start_button = page.locator(".share-mb-launcher")
             
        await start_button.click(timeout=10000)
        log("Dialog opened.")
        await asyncio.sleep(2)
        
        # Type content
        # Note: LinkedIn uses DraftJS/ProseMirror, so .fill() might not work perfectly. 
        # Using type() or inserting into innerText
        editor = page.locator("div[role='textbox']")
        await editor.focus()
        await editor.fill(post['text'])
        log("Text filled.")
        await asyncio.sleep(1)
        
        # Click Clock Icon
        log("Clicking scheduler icon...")
        await page.click("button[aria-label='Programmer pour plus tard']", timeout=5000)
        await asyncio.sleep(2)
        
        # Set Date
        log(f"Setting date to {post['iso_date']}...")
        await page.fill("input[type='date']", post['iso_date'])
        await asyncio.sleep(1)
        
        # Set Time
        log(f"Setting time to {post['time']}...")
        await page.fill("input[type='time']", post['time'])
        await asyncio.sleep(1)
        
        # Click Next
        log("Clicking 'Suivant'...")
        await page.get_by_role("button", name="Suivant").click()
        await asyncio.sleep(2)
        
        # Click Schedule
        log("Clicking 'Programmer'...")
        await page.get_by_role("button", name="Programmer").click()
        
        # Wait for confirmation toast/dialog to disappear
        await asyncio.sleep(5)
        log(f"Post {index} programmed successfully.")
        return True
    except Exception as e:
        log(f"Error on post {index}: {e}")
        await page.keyboard.press("Escape")
        await asyncio.sleep(2)
        return False

async def main():
    posts = parse_posts("tous_les_posts_linkedin.md")
    log(f"Parsed {len(posts)} posts.")
    
    async with async_playwright() as p:
        log("Connecting to Chrome...")
        # Connecting to the instance started with remote-debugging
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            
            for i, post in enumerate(posts, 1):
                success = await schedule_post(page, post, i)
                if not success:
                    log("Stopping due to error. Check browser state.")
                    break
                # Extra safety gap
                await asyncio.sleep(3)
                
            await browser.close()
        except Exception as e:
            log(f"Failed to connect or global error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
