import json
import aioredis
import fastapi as fa
import typing as t
from dto.courses import Courses
from core import cache

exchange_router_v1 = fa.APIRouter()


@exchange_router_v1.get(
    "/exchange/{symbol}", response_model=Courses, summary="Get symbol info (Version 1)"
)
async def get_symbol_info_v1(
    symbol: t.Optional[str] = "",
    redis_conn: aioredis.Redis = fa.Depends(cache.get_redis),
) -> t.Dict[str, t.Any]:
    data = {"exchange": "binance"}
    courses = []

    async with redis_conn.pipeline() as pipe:
        # Await the coroutine to get the actual Redis connection
        await pipe.keys(f"*{symbol}")
        pairs = await pipe.execute()

        for p in pairs[0]:
            courses.append(
                {"direction": p, "value": json.loads(await redis_conn.get(p))}
            )

    data["courses"] = courses
    return data
