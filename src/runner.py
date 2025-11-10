thonimport asyncio
import json
import logging
from src.extractors.twitter_parser import TwitterScraper
from src.outputs.exporters import JSONExporter
from src.config.settings import SETTINGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    tweet_url = input("Enter the Tweet URL: ").strip()
    if not tweet_url:
        logger.error("Tweet URL cannot be empty.")
        return

    scraper = TwitterScraper(cookies_file=SETTINGS['cookies_file'])
    try:
        comments = await scraper.scrape_comments(tweet_url)
        exporter = JSONExporter(output_file=SETTINGS['output_file'])
        exporter.export(comments)
        logger.info(f"Scraping completed. Output saved to {SETTINGS['output_file']}")
    except Exception as e:
        logger.exception(f"Error occurred during scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())