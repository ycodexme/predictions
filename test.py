import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl_result_handler import CrawlResultHandler
from html_result_handler import HtmlResultHandler
import json

async def scrape_predictions(crawler, base_url, prediction_type):
    url = f"{base_url}/today-football-predictions/{prediction_type}/"
    print(f"[DEBUG] Scraping URL: {url}")
    
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            word_count_threshold=10,
            excluded_tags=['form', 'header'],
            exclude_external_links=True,
            process_iframes=True,
            remove_overlay_elements=True,
            cache_mode=CacheMode.ENABLED,
            browser_args={
                'headless': True,
                'args': ['--no-sandbox', '--disable-setuid-sandbox']
            }
        )
    )
    
    if result.success:
        print(f"[DEBUG] Content length: {len(result.markdown)}")
        print(f"[DEBUG] First 200 chars: {result.markdown[:200]}")
    else:
        print(f"[ERROR] Failed to scrape {url}: {result.error_message}")
    
    return result

async def main():
    browser_config = BrowserConfig(
        verbose=True,
        browser_args={
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--single-process'
            ]
        }
    )
    json_handler = CrawlResultHandler()
    html_handler = HtmlResultHandler()

    base_url = "https://onemillionpredictions.com"
    results = {}

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # D'abord scraper la page d'accueil pour les prédictions 1X2
        print(f"[FETCH]... Scraping homepage (1X2)")
        home_result = await crawler.arun(
            url=base_url,
            config=CrawlerRunConfig(
                word_count_threshold=10,
                excluded_tags=['form', 'header'],
                exclude_external_links=True,
                process_iframes=True,
                remove_overlay_elements=True,
                cache_mode=CacheMode.ENABLED
            )
        )
        if home_result.success:
            results['1x2'] = home_result
        else:
            print(f"[ERROR]... Failed to scrape homepage: {home_result.error_message}")

        # Ensuite scraper les autres types de prédictions
        prediction_types = [
            'match-of-the-day',
            'top10',
            'accumulator-tips',
            'ht-ft-tips',
            'draw-no-bet',
            'double-chance',
            'special',
            'goalscorer',
            'both-teams-to-score',
            'correct-score',
            'cards',
            'corners',
            'goals'
        ]

        for pred_type in prediction_types:
            print(f"[FETCH]... Scraping {pred_type}")
            result = await scrape_predictions(crawler, base_url, pred_type)
            if result.success:
                results[pred_type.replace('-', '_')] = result
            else:
                print(f"[ERROR]... Failed to scrape {pred_type}: {result.error_message}")

        # Sauvegarder toutes les données
        if results:
            # Sauvegarder en JSON
            json_file = json_handler.save_result(results)
            print(f"[SAVE JSON]... ✓ Résultats sauvegardés dans {json_file}")

            # Charger les données JSON pour la conversion en HTML
            with open(json_file, 'r', encoding='utf-8') as f:
                result_data = json.load(f)

            # Sauvegarder en HTML
            html_file = html_handler.save_result(result_data)
            print(f"[SAVE HTML]... ✓ Page HTML générée dans {html_file}")

if __name__ == "__main__":
    asyncio.run(main())