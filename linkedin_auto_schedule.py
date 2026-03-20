import asyncio
from playwright.async_api import async_playwright
import datetime

POSTS = [
    {
        "text": "Les chatbots simples sont MORTS. En 2026, la révolution, ce sont les AGENTS AUTONOMES. Contrairement aux chatbots qui répondent, les agents agissent, planifient et utilisent vos outils. C'est ce que je fais avec Hassan, mon assistant OpenClaw. Et vous, votre IA parle ou agit ?\n#IA #AgentsIA #Automation #OpenClaw",
        "date": "16/02/2026",
        "time": "09:00"
    },
    {
        "text": "Plus gros n'est plus synonyme de meilleur. Les SLMs comme Phi-4 ou Mistral gagnent du terrain : Confidentialité (local), Vitesse (latence nulle), Coût réduit. Pas besoin d'un moteur de Boeing pour une citadine. Testez-vous des modèles locaux ?\n#SLM #MistralAI #EdgeComputing",
        "date": "17/02/2026",
        "time": "09:00"
    },
    {
        "text": "\"Garbage In, Garbage Out\". L'IA la plus puissante ne vaut rien sur des données corrompues. Le Data Cleaning est devenu une orchestration automatisée : détection d'anomalies en temps réel et déduplication intelligente. La qualité est votre socle.\n#DataQuality #DataEngineering #BigData",
        "date": "18/02/2026",
        "time": "09:00"
    },
    {
        "text": "Regagnez 10h par semaine. Les Agentic Workflows gèrent vos emails, extraient des insights de rapports massifs et planifient vos rendez-vous. Déléguez le répétitif pour libérer votre créativité. Quelle tâche délégueriez-vous à un gorille numérique ? 🦍\n#Automation #Productivité #HassanTheGorilla",
        "date": "19/02/2026",
        "time": "09:00"
    },
    {
        "text": "Fini les pipelines rigides, place à l'Orchestration Dynamique. Auto-healing, scaling prédictif et interconnexion totale. Le Data Engineer devient architecte de flux. Prêt pour l'étape suivante ?\n#DataEngineering #ModernDataStack #Infrastructure",
        "date": "20/02/2026",
        "time": "09:00"
    }
]

import sys

def print_flush(text):
    print(text)
    sys.stdout.flush()

async def main():
    async with async_playwright() as p:
        print_flush("Connecting to Chrome on 9222...")
        # ... rest of code replacing print with print_flush ...
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("Navigating to LinkedIn...")
        await page.goto("https://www.linkedin.com/feed/")
        await asyncio.sleep(5) # Wait for page load
        
        for post in POSTS:
            print(f"Programming post: {post['date']} at {post['time']}...")
            try:
                # Click start post
                await page.click("button.share-mb-launcher", timeout=10000)
                await asyncio.sleep(2)
                
                # Type text
                await page.fill("div[role='textbox']", post['text'])
                await asyncio.sleep(1)
                
                # Click clock icon
                await page.click("button[aria-label='Programmer pour plus tard']")
                await asyncio.sleep(2)
                
                # Set date and time
                # The date input usually has a specific class or placeholder
                # This is fragile but we'll try common selectors
                date_input = page.locator("input[type='date']")
                time_input = page.locator("input[type='time']")
                
                # Convert date format if needed (DD/MM/YYYY to YYYY-MM-DD for input)
                d, m, y = post['date'].split('/')
                iso_date = f"{y}-{m}-{d}"
                
                await date_input.fill(iso_date)
                await time_input.fill(post['time'])
                await asyncio.sleep(1)
                
                # Click Next
                await page.click("button:has-text('Suivant')")
                await asyncio.sleep(1)
                
                # Click Schedule
                await page.click("button:has-text('Programmer')")
                await asyncio.sleep(3)
                print(f"Success for {post['date']}")
                
            except Exception as e:
                print(f"Failed for {post['date']}: {e}")
                # Try to close dialog if stuck
                try: await page.click("button[aria-label='Ignorer']", timeout=2000)
                except: pass

        print("Finished Week 1.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
