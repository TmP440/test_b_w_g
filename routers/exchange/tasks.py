import aioredis
import typing as t
import json


async def cache_data_in_background(
    redis_conn: aioredis.Redis, courses: t.List[t.Dict[str, t.Any]]
):
    for course in courses:
        await redis_conn.set(course["direction"], json.dumps(course["value"]))
