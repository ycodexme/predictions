import asyncio
import os
import subprocess
from datetime import datetime
from test import main as scrape_main

async def build():
    # Créer le dossier dist s'il n'existe pas
    os.makedirs('dist', exist_ok=True)
    
    # Installer les navigateurs Playwright
    print("Installing Playwright browsers...")
    subprocess.run(["playwright", "install", "chromium", "--with-deps"], check=True)
    
    # Définir les variables d'environnement pour le mode headless
    os.environ["PLAYWRIGHT_CHROMIUM_EXECUTABLE"] = ""
    os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "1"
    
    # Lancer le scraping
    await scrape_main()
    
    # Déplacer le fichier HTML généré vers dist/index.html
    latest_html = max(
        [f for f in os.listdir('.') if f.startswith('football_predictions_') and f.endswith('.html')],
        key=os.path.getctime
    )
    
    os.rename(latest_html, 'dist/index.html')
    
    # Créer un fichier netlify.toml
    netlify_config = """
[build]
  publish = "dist"
  command = "python build.py"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
    """
    
    with open('netlify.toml', 'w') as f:
        f.write(netlify_config)
    
    # Créer un fichier requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write("""
crawl4ai==0.4.248
aiohttp==3.8.5
beautifulsoup4==4.12.2
        """.strip())

if __name__ == "__main__":
    asyncio.run(build()) 