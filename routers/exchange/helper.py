import aioredis
import json
from sqlalchemy import orm
from routers.exchange.queries import get_all_pairs


async def get_info_from_cache(redis_conn: aioredis.Redis, symbol: str):
    courses = []

    async with redis_conn.pipeline() as pipe:
        await pipe.keys(f"*{symbol}")
        pairs = await pipe.execute()

        for p in pairs[0]:
            courses.append(
                {"direction": p, "value": json.loads(await redis_conn.get(p))}
            )
        return courses


async def storing_info_in_cache(symbol: str, db: orm.Session):
    courses = []
    db_data = get_all_pairs(symbol, db)

    for db_entry in db_data:
        courses.append({"direction": db_entry.symbol, "value": db_entry.price})
    return courses
