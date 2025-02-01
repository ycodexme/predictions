import os
import shutil

def build():
    # Créer le dossier dist s'il n'existe pas
    os.makedirs('dist', exist_ok=True)
    
    # Copier le fichier HTML le plus récent vers dist/index.html
    latest_html = max(
        [f for f in os.listdir('.') if f.startswith('football_predictions_') and f.endswith('.html')],
        key=os.path.getctime
    )
    
    shutil.copy2(latest_html, 'dist/index.html')

if __name__ == "__main__":
    build() 