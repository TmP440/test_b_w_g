import aioredis


async def get_redis() -> aioredis.Redis:
    redis_db = await aioredis.from_url(
        "redis://127.0.0.1:6379",
        encoding="utf-8",
    )
    return redis_db


async def close_redis(redis: aioredis.Redis) -> None:
    await redis.close()


async def set_price(symbol: str, price: str) -> None:
    redis = await get_redis()
    try:
        await redis.set(symbol, price)
    finally:
        await close_redis(redis)


async def get_price(symbol: str) -> float:
    redis = await get_redis()
    try:
        price = await redis.get(symbol)
        return float(price) if price is not None else 0.0
    finally:
        await close_redis(redis)
