import asyncio
from playwright.async_api import async_playwright
import datetime
import sys

def log(text):
    print(f"[{datetime.datetime.now()}] {text}")
    sys.stdout.flush()

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

async def main():
    async with async_playwright() as p:
        log("Connecting to Chrome on 9222...")
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            log("Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/feed/", wait_until="networkidle")
            await page.screenshot(path="linkedin_debug.png")
            log("Debug screenshot saved.")
            
            for i, post in enumerate(POSTS):
                log(f"--- Post {i+1}/5: {post['date']} ---")
                try:
                    # Start post
                    await page.click("button:has-text('Commencer un post')", timeout=15000)
                    log("Opened post dialog")
                    
                    # Fill text
                    await page.fill("div[role='textbox']", post['text'])
                    log("Filled text")
                    
                    # Schedule
                    await page.click("button[aria-label='Programmer pour plus tard']", timeout=5000)
                    log("Opened scheduler")
                    
                    # Date & Time
                    d, m, y = post['date'].split('/')
                    iso_date = f"{y}-{m}-{d}"
                    
                    await page.fill("input[type='date']", iso_date)
                    await page.fill("input[type='time']", post['time'])
                    log(f"Set schedule to {post['date']} {post['time']}")
                    
                    # Next
                    await page.click("button:has-text('Suivant')")
                    log("Clicked Next")
                    
                    # Schedule Button
                    await page.click("button:has-text('Programmer')")
                    log("Clicked Schedule")
                    
                    await asyncio.sleep(5)
                    log(f"Successfully programmed Post {i+1}")
                    
                except Exception as e:
                    log(f"Error on Post {i+1}: {e}")
                    # Escape dialog
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(2)
            
            log("Finished sequence.")
            await page.close()
            
        except Exception as e:
            log(f"Global error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
