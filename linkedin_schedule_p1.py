import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        # Connect to existing Chrome with remote debugging
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            print("Connected to Chrome. Navigating to LinkedIn...")
            await page.goto("https://www.linkedin.com/feed/")
            await page.wait_for_load_state("networkidle")

            # Click Start Post
            print("Opening post dialog...")
            await page.click("button.share-mb-launcher")
            
            # Post Text
            text = """Les chatbots simples sont MORTS. 💀

En 2026, si vous \"discutez\" encore avec une IA qui attend vos ordres, vous avez déjà un train de retard. 

La révolution actuelle, ce sont les **AGENTS AUTONOMES**. 🚀

Contrairement aux chatbots qui se contentent de répondre, les agents :
✅ Raisonnent par eux-mêmes.
✅ Planifient des séquences d'actions complexes.
✅ Utilisent vos outils (navigateur, APIs, bases de données) pour exécuter des tâches de bout en bout.

C'est exactement ce que je fais avec Hassan, mon assistant OpenClaw. Il ne se contente pas de rédiger, il agit. 🦍

**Et vous, votre IA elle parle ou elle agit ?** 🧐

#IA #AgentsIA #Automation #OpenClaw #Productivité #FutureOfWork"""
            
            await page.fill("div[role='textbox']", text)
            
            # Upload Image
            print("Uploading image...")
            async with page.expect_file_chooser() as fc_info:
                await page.click("button[aria-label='Ajouter un média']")
            file_chooser = await fc_info.value
            await file_chooser.set_files(r"C:\Users\zkhch\.openclaw\workspace\linkedin_images\post1.jpg")
            
            await page.wait_for_selector("button:has-text('Suivant')")
            await page.click("button:has-text('Suivant')")
            
            # Schedule
            print("Opening scheduler...")
            await page.click("button[aria-label='Programmer pour plus tard']")
            
            # Set Date (Next Monday Feb 16)
            # This is hard to automate precisely without knowing the specific date picker structure, 
            # so we'll try to find the inputs.
            # Usually it's an input type date or similar.
            
            print("Finished preparation. User should check the scheduler dialog.")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
