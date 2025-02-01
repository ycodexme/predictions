import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

class HtmlResultHandler:
    def __init__(self):
        self.filename_prefix = "football_predictions"
        self.prediction_types = {
            '1x2': {
                'icon': '🎯',
                'name': '1X2',
                'description': 'Paris sur le résultat final du match (Victoire, Nul, Défaite)'
            },
            'match_of_the_day': {
                'icon': '🌟',
                'name': 'Match du Jour',
                'description': 'Sélection premium du jour avec la meilleure analyse'
            },
            'top10': {
                'icon': '🔝',
                'name': 'Top 10 Prédictions',
                'description': 'Les 10 meilleures prédictions du jour'
            },
            'accumulator_tips': {
                'icon': '💫',
                'name': 'Combinés (ACCA)',
                'description': 'Combinaisons de paris à forte valeur'
            },
            'ht_ft_tips': {
                'icon': '⏱️',
                'name': 'Mi-temps/Fin de match',
                'description': 'Prédictions sur les scores à la mi-temps et fin de match'
            },
            'draw_no_bet': {
                'icon': '🛡️',
                'name': 'Draw No Bet (DNB)',
                'description': 'Paris avec remboursement en cas de match nul'
            },
            'double_chance': {
                'icon': '2️⃣',
                'name': 'Double Chance',
                'description': 'Deux résultats possibles sur trois'
            },
            'special': {
                'icon': '✨',
                'name': 'Prédictions Spéciales',
                'description': 'Sélections spéciales avec analyse approfondie'
            },
            'goalscorer': {
                'icon': '⚽',
                'name': 'Buteurs',
                'description': 'Prédictions sur les buteurs du match'
            },
            'both_teams_to_score': {
                'icon': '🥅',
                'name': 'Les Deux Équipes Marquent (BTTS)',
                'description': 'Prédictions sur les buts des deux équipes'
            },
            'correct_score': {
                'icon': '📊',
                'name': 'Score Exact',
                'description': 'Prédictions du score final exact'
            },
            'cards': {
                'icon': '🟨',
                'name': 'Cartons',
                'description': 'Prédictions sur les cartons jaunes et rouges'
            },
            'corners': {
                'icon': '🚩',
                'name': 'Corners',
                'description': 'Prédictions sur le nombre de corners'
            },
            'goals': {
                'icon': '⚽',
                'name': 'Buts',
                'description': 'Prédictions sur le nombre de buts'
            }
        }
        self.template_css = """
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --background-color: #f9f9f9;
            --text-color: #333;
            --border-color: #ddd;
        }

        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--background-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
        }

        .league-section {
            background: white;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .league-header {
            background: var(--secondary-color);
            color: white;
            padding: 15px;
        }

        .league-header h2 {
            margin: 0;
            font-size: 1.2em;
        }

        .match-teams {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .team-home {
            flex: 1;
            text-align: right;
        }

        .team-away {
            flex: 1;
            text-align: left;
        }

        .vs {
            color: #3498db;  /* bleu */
            font-weight: normal;
            padding: 0 5px;
        }

        .odds-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            justify-content: end;
            min-width: 200px;
        }

        .odd-box {
            text-align: center;
            font-weight: bold;
            background: #f8f9fa;
            padding: 5px 10px;
            border-radius: 4px;
        }

        td:first-child {  /* Colonne heure */
            color: #e74c3c;  /* rouge */
            width: 100px;
        }

        td:nth-child(2) {  /* Colonne match */
            width: auto;
            padding-right: 30px;
        }

        td:last-child {  /* Colonne cotes */
            width: 250px;
        }

        th {
            font-weight: bold;
            color: #2c3e50;
            padding: 15px 12px;
            background: #f8f9fa;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }

        tr:hover {
            background-color: #f5f8fa;
        }

        .metadata {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
            }
        }

        .predictions-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .prediction-type-btn {
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            background: #f0f2f5;
            cursor: pointer;
            transition: all 0.3s;
        }

        .prediction-type-btn:hover {
            background: var(--secondary-color);
            color: white;
        }

        .prediction-type-btn.active {
            background: var(--primary-color);
            color: white;
        }

        .prediction-section {
            display: none;
        }

        .prediction-section.active {
            display: block;
        }

        .prediction-header {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .prediction-description {
            color: #666;
            margin: 10px 0 0;
            font-size: 0.9em;
        }

        .prediction-type-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 15px;
            font-size: 0.9em;
            white-space: nowrap;
        }

        .predictions-nav {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        """

    def _split_teams(self, teams_str: str) -> tuple:
        """Sépare la chaîne des équipes en équipe domicile et extérieur"""
        # Supprimer les espaces inutiles
        teams_str = teams_str.strip()
        
        # Trouver la position où la deuxième équipe commence
        # en cherchant la première lettre majuscule après quelques caractères
        for i in range(3, len(teams_str)):
            if teams_str[i].isupper():
                return teams_str[:i].strip(), teams_str[i:].strip()
        
        # Si pas de séparation trouvée, retourner la chaîne entière comme équipe domicile
        return teams_str, ""

    def generate_html(self, result_data: Dict) -> str:
        print(f"[DEBUG] Available prediction types in data: {result_data['metadata']['prediction_types']}")
        print(f"[DEBUG] Total matches: {len(result_data['matches'])}")
        
        # Grouper les matches par type de prédiction et par ligue
        predictions_by_type = {}
        for match in result_data['matches']:
            pred_type = match['prediction_type']
            if pred_type not in predictions_by_type:
                predictions_by_type[pred_type] = {}
            
            league = match['league']
            if league not in predictions_by_type[pred_type]:
                predictions_by_type[pred_type][league] = []
            
            predictions_by_type[pred_type][league].append(match)

        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Prédictions de football mises à jour quotidiennement">
            <meta name="keywords" content="football, prédictions, paris sportifs, 1X2, match du jour">
            <title>Prédictions Football</title>
            <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA7AAAAOwBeShxvQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAL0SURBVFiF7ZdNiFZVGMd/z7lvM42NhY0fA4MutJAkyGhRi8BGELJFuBKCFi1aJERBq2jTIoQgaBG0CTdBQUSrwE0QgRQYFhFE0YczfeAwOvk5fszce57/LO6dO/e+7zsz7zsK0R8u73PO89zz/M/5P+c+F/7nyCRO9UTjBVWdrar3i8hDqtopIjNF5JKInBeR4yLyg4gcCcPwz4bxVPV+EXlYVeeJyF0iclNELovISVX9XkQOh2F4pZ58Mj4+Xv2uqpOBV4EPgKmN5r4JfAG8HgTB9VqnariqPgp8BsxpGLk2TgEbwjD8thp+W3hVXQZ8STp4D7BWVR9Q1WlZTFWdpqoPqupaYA/pAr0LfKWqK6rhN9OiqncCx4BZwDFgUxiGh+sEfwxYD6wApgC/AcvDMDyTjlmiqn3ALcABngzD8GS1r6r2AHuBhcBBYEMYhtfrwMeBd4AngWnACWB1GIbHq2IsBl4SkS4R6QF2A6+EYXiz2i8Mw9+BZ4HfgUXA+8BzqjqnTowlwOfAbOAQ8EwYhhdvg6vqVBHZAXwI3AF8DKyqhkMy+L8iskFVHwO+A7qAT1V1ZaOJUtX1wA5gMvApsD4Mw5Fa/qp6l4h8A7wNBMAHYRi+VM8XoA/oBw4Aa8MwHK3nXIVfCewCWoFdwAtBEIzV81fVNuBLYDlwGFgThuGlevFUdTqwG1gKHAfWhWF4oZG/iMwQkb3AE8CvwKowDH9q5J+JsQzYCUwBvgaeDcNwqFEMVZ0L7APmAWeA1WEY/tJovExz+oEW4AtgfRiGN+r5q2oH8BmwGhgBXg3DcHsz8TPNOQTcC+wHng/DcKSWv6q2Ax8BzwEjwFtBEHzUbPxMc34E7gH2Ak83gk8D9gGPAkPApjAMP24mfhZjPnAEaAfeBd5oYPk7gS3AJmAMeDsMw/ebja+qU0TkbRG5ISKbReT5IAj+quXfjOZkPu0i8qSI9IrIYhGZKSKXROSciPwsIj+JyNEgCP5uNt7/HP8A/ZmTxKiQ+lMAAAAASUVORK5CYII=">
            <style>{self.template_css}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚽ Prédictions Football</h1>
                    <p>Mis à jour le {datetime.fromisoformat(result_data['metadata']['timestamp']).strftime('%d/%m/%Y à %H:%M')}</p>
                </div>

                <div class="predictions-nav">
        """

        # Ajouter les boutons de navigation
        for pred_type, info in self.prediction_types.items():
            if pred_type in predictions_by_type:
                html += f"""
                    <button class="prediction-type-btn" onclick="showPrediction('{pred_type}')">
                        {info['icon']} {info['name']}
                    </button>
                """

        html += """
                </div>
        """

        # Générer les sections pour chaque type de prédiction
        for pred_type, leagues in predictions_by_type.items():
            info = self.prediction_types[pred_type]
            html += f"""
                <div id="{pred_type}" class="prediction-section">
                    <div class="prediction-header">
                        <h2>{info['icon']} {info['name']}</h2>
                        <p class="prediction-description">{info['description']}</p>
                    </div>
            """

            for league_name, matches in leagues.items():
                html += self._generate_league_section(league_name, matches)

            html += """
                </div>
            """

        # Ajouter le JavaScript pour la navigation
        html += """
                <script>
                function showPrediction(predType) {
                    // Cacher toutes les sections
                    document.querySelectorAll('.prediction-section').forEach(section => {
                        section.classList.remove('active');
                    });
                    // Afficher la section sélectionnée
                    document.getElementById(predType).classList.add('active');
                    
                    // Mettre à jour les boutons
                    document.querySelectorAll('.prediction-type-btn').forEach(btn => {
                        btn.classList.remove('active');
                    });
                    event.target.classList.add('active');
                }

                // Afficher la première section au chargement
                document.addEventListener('DOMContentLoaded', function() {
                    const firstButton = document.querySelector('.prediction-type-btn');
                    if (firstButton) {
                        firstButton.click();
                    }
                });
                </script>
            </div>
        </body>
        </html>
        """
        
        return html

    def _generate_league_section(self, league_name: str, matches: List[Dict]) -> str:
        """Génère le HTML pour une section de ligue"""
        html = f"""
            <div class="league-section">
                <div class="league-header">
                    <h2>🏆 {league_name}</h2>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Heure</th>
                            <th>Match</th>
                            <th>Cotes</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for match in matches:
            home_team, away_team = self._split_teams(match['teams'])
            
            # Générer l'affichage des cotes selon le type de prédiction
            odds_html = self._generate_odds_html(match)
            
            html += f"""
                        <tr>
                            <td>{match['datetime']}</td>
                            <td>
                                <div class="match-teams">
                                    <span class="team-home">{home_team}</span>
                                    <span class="vs">vs</span>
                                    <span class="team-away">{away_team}</span>
                                </div>
                            </td>
                            <td>
                                <div class="odds-container">
                                    {odds_html}
                                </div>
                            </td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        """
        return html

    def _generate_odds_html(self, match: Dict) -> str:
        """Génère le HTML pour les cotes selon le type de prédiction"""
        prediction_type = match['prediction_type']
        odds = match['odds']
        
        if prediction_type in ['goals', 'corners', 'cards']:
            return f"""
                <div class="odd-box">{odds.get('line', 'N/A')}</div>
                <div class="odd-box">Over {odds.get('over', 'N/A')}</div>
                <div class="odd-box">Under {odds.get('under', 'N/A')}</div>
            """
        elif prediction_type == 'both_teams_to_score':
            return f"""
                <div class="odd-box">Yes {odds.get('yes', 'N/A')}</div>
                <div class="odd-box">No {odds.get('no', 'N/A')}</div>
            """
        elif prediction_type == 'correct_score':
            return f"""
                <div class="odd-box">{odds.get('score', 'N/A')}</div>
                <div class="odd-box">{odds.get('odds', 'N/A')}</div>
            """
        elif prediction_type == 'match_of_the_day':
            return f"""
                <div class="odd-box">{odds.get('1', 'N/A')}</div>
            """
        else:
            # Format par défaut pour les autres types (1X2)
            return f"""
                <div class="odd-box">{odds.get('1', 'N/A')}</div>
                <div class="odd-box">{odds.get('X', 'N/A')}</div>
                <div class="odd-box">{odds.get('2', 'N/A')}</div>
            """

    def save_result(self, result_data: Dict) -> str:
        """Sauvegarde le résultat en HTML"""
        html_content = self.generate_html(result_data)
        filename = f"{self.filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return filename 