import os

import redis.asyncio as redis

from app import settings

global_settings = settings.get_settings()


async def get_redis():
    return await redis.from_url(
        global_settings.redis_url.unicode_string(),
        encoding="utf-8",
        decode_responses=True,
    )
