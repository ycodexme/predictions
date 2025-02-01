import os
import shutil

def build():
    # Créer le dossier dist s'il n'existe pas
    os.makedirs('dist', exist_ok=True)
    
    # Chercher les fichiers HTML de prédictions
    html_files = [f for f in os.listdir('.') if f.startswith('football_predictions_') and f.endswith('.html')]
    
    if html_files:
        # Si on trouve des fichiers, prendre le plus récent
        latest_html = max(html_files, key=os.path.getctime)
        shutil.copy2(latest_html, 'dist/index.html')
        print(f"Copié {latest_html} vers dist/index.html")
    else:
        # Si aucun fichier n'est trouvé, créer une page par défaut
        default_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Football Predictions</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Football Predictions</h1>
            <p>Les prédictions seront bientôt disponibles.</p>
        </body>
        </html>
        """
        with open('dist/index.html', 'w', encoding='utf-8') as f:
            f.write(default_html)
        print("Créé une page par défaut dans dist/index.html")

if __name__ == "__main__":
    build() 