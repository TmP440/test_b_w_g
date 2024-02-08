import aioredis
import fastapi as fa
from fastapi.responses import JSONResponse
from core.metics import save_status_code_in_influxdb
import typing
from dto.courses import Courses
from core import cache
from core.logs import log
from routers.exchange import helper as exchange_helper
from routers.exchange import tasks as exchange_task
from config import settings

exchange_router_v1 = fa.APIRouter()


@exchange_router_v1.get(
    "/exchange", response_model=Courses, summary="Get symbol info (Version 1)"
)
async def get_symbol_info_v1(
    symbol: typing.Optional[str] = "",
    redis_conn: aioredis.Redis = fa.Depends(cache.get_redis),
) -> JSONResponse:
    symbol = symbol.upper()
    try:
        if symbol.lower() not in settings.coin_pairs and symbol != "":
            await save_status_code_in_influxdb("/api/v1/exchange", "400")
            return JSONResponse(
                content={"status_code": 400, "message": "Invalid symbol"},
                status_code=400,
            )

        exchanger_name = await cache.get_exchanger_name()
        data = {"exchange": str(exchanger_name)}

        courses = await exchange_helper.get_info_from_cache(redis_conn, symbol)

        if not courses:
            courses = await exchange_helper.storing_info_in_cache(symbol)
            if courses:
                await exchange_task.cache_data_in_background(redis_conn, courses)

        data["courses"] = courses
        await save_status_code_in_influxdb("/api/v1/exchange", "200")
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        await save_status_code_in_influxdb("/api/v1/exchange", "500")
        log.error(f"Server error: {e}")
        return JSONResponse(
            content={"status_code": 500, "message": "Internal Server Error"},
            status_code=500,
        )
