import asyncio
import json
import logging
from binance.client import AsyncClient
from core import cache

API_KEY = "j4R4t82xbWMl1DYVViKTcQV72T6ncll2AThtxW5P5PbsWNjsuJDEzdsCWYbURu4B"
SECRET_KEY = "8lTDhpCsmYH3xzXlgXhDMFaU7lzDNPJpt9Jzv71y3plMCgLEoSceiRYR6ycqjgaq"

COIN_PAIRS = [
    "BTCUSDT",
    "BTCRUB",
    "ETHUSDT",
    "ETHRUB",
    "USDTTRCUSDT",
    "USDTTRCRUB",
    "USDTERCUSDT",
    "USDTERCRUB",
]

logging.basicConfig(filename="app.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def update_info():
    try:
        client = await AsyncClient.create(API_KEY, SECRET_KEY)
        redis = await cache.get_redis()

        while True:
            for pair in COIN_PAIRS:
                try:
                    res = await client.get_avg_price(
                        symbol=pair, requests_params={"timeout": 2}
                    )
                    await cache.set_price(pair, json.dumps(res["price"]))
                    print(pair, res)
                except Exception as e:
                    logger.error(f"Ошибка при обновлении цены для {pair}: {e}")
                    print("Error!")

            await redis.close()
            await asyncio.sleep(5)
    except Exception as e:
        # Замена print на логгирование
        logger.error(f"Ошибка в основном цикле: {e}")
