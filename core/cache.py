import aioredis
import json

import config
from core.logs import log


async def get_redis() -> aioredis.Redis:
    redis_db = await aioredis.from_url(
        "redis://127.0.0.1:6379/1",
        encoding="utf-8",
    )
    return redis_db


async def close_redis(redis: aioredis.Redis) -> None:
    await redis.close()


async def set_value(symbol: str, value: str) -> None:
    redis = await get_redis()
    try:
        await redis.set(symbol, value)
    finally:
        log.info(f"successful saved in cache: {symbol} - {value}")
        await close_redis(redis)


async def get_exchanger_name() -> str:
    redis = await get_redis()
    exchanger_name = await redis.get("exchanger")
    return exchanger_name.decode("utf-8")


async def get_value(symbol: str) -> float:
    redis = await get_redis()
    try:
        price = await redis.get(symbol)
        return float(price) if price is not None else 0.0
    finally:
        await close_redis(redis)


async def message_handler(msg):
    log.info(f"message received: {msg}")
    log.info(f"Start saving to cache")
    json_data = msg.data.decode()
    data_dict = json.loads(json_data)
    await set_value(data_dict["pair"], data_dict["price"])
