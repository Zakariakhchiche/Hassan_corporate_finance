import asyncio
from playwright.async_api import async_playwright
import datetime
import sys

def log(text):
    print(f"[{datetime.datetime.now()}] {text}")
    sys.stdout.flush()

async def main():
    async with async_playwright() as p:
        log("Connecting to Chrome on 9222...")
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            await page.goto("https://www.linkedin.com/feed/")
            await asyncio.sleep(5)
            await page.screenshot(path="linkedin_check_login.png")
            log("Screenshot saved to linkedin_check_login.png")
            await browser.close()
        except Exception as e:
            log(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
