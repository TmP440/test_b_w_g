import asyncio
import json
import logging
from binance.client import AsyncClient
from aiokafka import AIOKafkaProducer
from core import cache
from config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

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
        print("ya tut")
        client = await AsyncClient.create(API_KEY, SECRET_KEY)
        print(client)
        try:
            producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
            await producer.start()
            print("Uspeshno!")
        except Exception as ex:
            logger.error(f"Не удалось подключиться к продюсеру: {ex}")
            print("Не удалось подключиться к прод.серу")
            print(ex)

        while True:
            print("while")
            for pair in COIN_PAIRS:
                print("pair")
                try:
                    res = await client.get_avg_price(
                        symbol=pair, requests_params={"timeout": 2}
                    )
                    print(res)
                    message = json.dumps({"pair": pair, "price": res["price"]})
                    await producer.send_and_wait(KAFKA_TOPIC, value=message.encode())
                    await cache.set_price(pair, json.dumps(res["price"]))
                except Exception as e:
                    logger.error(f"Ошибка при обновлении цены для {pair}: {e}")

            await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Ошибка в основном цикле: {e}")
