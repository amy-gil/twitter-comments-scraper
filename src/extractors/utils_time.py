thonimport asyncio
import random

async def random_delay(min_seconds: int = 1, max_seconds: int = 3):
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)