import json
from datetime import datetime
from typing import Dict, Any, List

class CrawlResultHandler:
    def __init__(self):
        self.filename_prefix = "football_predictions"
        self.prediction_types = {
            'match_of_the_day': 'Match of the Day',
            'top10': 'Top 10 Predictions',
            'accumulator': 'Accumulator Tips',
            'ht_ft': 'HT/FT Tips',
            'draw_no_bet': 'Draw No Bet',
            'double_chance': 'Double Chance',
            'special': 'Special Predictions',
            'goalscorer': 'Goalscorer',
            'btts': 'Both Teams to Score',
            'correct_score': 'Correct Score',
            'cards': 'Cards',
            'corners': 'Corners',
            'goals': 'Goals'
        }

    def _parse_matches(self, content: str, prediction_type: str) -> List[Dict]:
        matches = []
        current_league = None
        
        print(f"[DEBUG] Analyzing content for {prediction_type}")
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                
                # Ignorer les lignes d'en-tête et de séparation
                if '-+-' in line or not parts[0] or parts[0].startswith('Kick Off'):
                    continue
                
                # Détecter une ligne de ligue
                if len(parts) >= 3 and ' - ' in parts[0]:
                    if not any(x in parts[0] for x in ['1', 'X', '2', 'Goals', 'Cards', 'Corners']):
                        current_league = parts[0]
                        print(f"[DEBUG] Found league: {current_league}")
                    continue
                
                # Détecter un match selon le type de prédiction
                if current_league and len(parts) >= 3:
                    if parts[0] and parts[0][0].isdigit():
                        try:
                            match = {
                                'league': current_league,
                                'datetime': parts[0],
                                'teams': parts[1],
                                'prediction_type': prediction_type,
                                'odds': self._parse_odds(parts, prediction_type),
                                'additional_info': self._get_additional_info(prediction_type, parts)
                            }
                            matches.append(match)
                            print(f"[DEBUG] Found match: {match['teams']}")
                        except Exception as e:
                            print(f"[ERROR] Parsing match failed at line {i}: {e}")
                            continue

        return matches

    def _parse_odds(self, parts: List[str], prediction_type: str) -> Dict[str, str]:
        """Parse les cotes selon le type de prédiction"""
        odds = {}
        try:
            if prediction_type == 'match_of_the_day':
                odds = {'1': parts[2].strip()}
            elif prediction_type == 'correct_score':
                odds = {'score': parts[2].strip(), 'odds': parts[3].strip()}
            elif prediction_type == 'both_teams_to_score':
                odds = {'yes': parts[2].strip(), 'no': parts[3].strip()}
            elif prediction_type in ['goals', 'corners', 'cards']:
                odds = {
                    'line': parts[2].strip(),
                    'over': parts[3].strip(),
                    'under': parts[4].strip()
                }
            else:
                odds = {
                    '1': parts[2].strip() if len(parts) > 2 else 'N/A',
                    'X': parts[3].strip() if len(parts) > 3 else 'N/A',
                    '2': parts[4].strip() if len(parts) > 4 else 'N/A'
                }
        except Exception as e:
            print(f"[ERROR] Parsing odds failed for {prediction_type}: {e}")
            odds = {'error': str(e)}
        return odds

    def _get_additional_info(self, prediction_type: str, parts: List[str]) -> Dict:
        """Récupère les informations additionnelles selon le type de prédiction"""
        info = {}
        try:
            if prediction_type == 'match_of_the_day':
                info['confidence'] = 'High'
            elif prediction_type == 'top10':
                info['rank'] = parts[1].split('.')[0] if '.' in parts[1] else 'N/A'
            elif prediction_type == 'accumulator_tips':
                info['combined_odds'] = parts[-1] if len(parts) > 3 else 'N/A'
            elif prediction_type == 'ht_ft_tips':
                info['ht_prediction'] = parts[2] if len(parts) > 2 else 'N/A'
                info['ft_prediction'] = parts[3] if len(parts) > 3 else 'N/A'
        except Exception as e:
            print(f"[ERROR] Getting additional info failed: {e}")
        return info

    def generate_filename(self) -> str:
        """Génère un nom de fichier unique avec horodatage"""
        return f"{self.filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def prepare_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prépare les données à partir de plusieurs résultats de scraping"""
        all_matches = []
        
        print(f"[DEBUG] Processing {len(results)} prediction types")  # Debug
        
        for prediction_type, result in results.items():
            matches = self._parse_matches(result.markdown, prediction_type)
            all_matches.extend(matches)

        print(f"[DEBUG] Total matches found: {len(all_matches)}")  # Debug
        print(f"[DEBUG] Prediction types found: {set(match['prediction_type'] for match in all_matches)}")  # Debug

        return {
            'url': 'https://onemillionpredictions.com',
            'matches': all_matches,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_matches': len(all_matches),
                'prediction_types': sorted(list(set(match['prediction_type'] for match in all_matches))),
                'leagues': sorted(list(set(match['league'] for match in all_matches))),
                'last_update': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        }
    
    def save_result(self, result) -> str:
        """Sauvegarde les résultats dans un fichier JSON"""
        filename = self.generate_filename()
        data = self.prepare_data(result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return filename 