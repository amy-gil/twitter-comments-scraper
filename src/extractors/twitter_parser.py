thonimport asyncio
import json
import logging
from typing import List, Dict
from src.extractors.utils_time import random_delay
from aiohttp import ClientSession, CookieJar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self, cookies_file: str):
        self.cookies_file = cookies_file
        self.cookies = self._load_cookies()

    def _load_cookies(self) -> Dict:
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return {}

    async def fetch_json(self, url: str, session: ClientSession):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def scrape_comments(self, tweet_url: str) -> List[Dict]:
        # Simple ID extraction
        tweet_id = tweet_url.strip('/').split('/')[-1]
        api_url = f"https://api.twitter.com/2/timeline/conversation/{tweet_id}.json"

        jar = CookieJar()
        async with ClientSession(cookies=self.cookies, cookie_jar=jar) as session:
            data = await self.fetch_json(api_url, session)

        comments = []
        for item in data.get('comments', []):
            comment = {
                "conversation_id_str": item.get("conversation_id_str"),
                "full_text": item.get("full_text"),
                "user": item.get("user"),
                "favorite_count": item.get("favorite_count"),
                "reply_count": item.get("reply_count"),
                "retweet_count": item.get("retweet_count"),
                "created_at": item.get("created_at"),
                "entities": item.get("entities", {})
            }
            comments.append(comment)
            await random_delay(1, 3)
        return comments