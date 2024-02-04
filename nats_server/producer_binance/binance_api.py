import requests
import asyncio
import json
import logging
from nats.aio.client import Client as NATS
from binance.client import AsyncClient
from core import cache
from nats_server.tasks import save_db
from core.logs import log
from config import (
    nats_host,
    nats_port,
    nats_subject,
    API_KEY,
    SECRET_KEY,
    convert_pairs_to_CG_syntax,
    COIN_PAIRS,
)

logging.basicConfig(filename="app.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def get_pair_info(pair: str, client=None):
    try:
        res = await client.get_avg_price(symbol=pair, requests_params={"timeout": 2})
        log.info(f"Binance returned price: {pair}: {res['price']}")
        await cache.set_value("exchanger", "binance")
        return res
    except Exception as e:
        log.info("Binance is not active")
        try:
            ids, vs_currencies = (
                convert_pairs_to_CG_syntax[pair]["id"],
                convert_pairs_to_CG_syntax[pair]["currencies"],
            )
            base_url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": ids,
                "vs_currencies": vs_currencies,
            }
            response = requests.get(
                f"{base_url}?ids={params['ids']}&vs_currencies={params['vs_currencies']}"
            )
            data = response.json()
            print(f"\n\n{data}\n\n")
            log.info(f"Coingeko returned price: {pair} {data[ids][vs_currencies]}")
            await cache.set_value("exchanger", "coingeko")
            return {"price": data[ids][vs_currencies]}
        except Exception as e:
            log.critical(f"Coingeko is not active too!!!")
            log.exception(e)


async def update_info():
    try:
        client = await AsyncClient.create(API_KEY, SECRET_KEY)
        nc = NATS()
        await nc.connect(servers=[nats_host + ":" + nats_port])
        sub1 = await nc.subscribe(nats_subject, cb=save_db.message_handler)
        sub2 = await nc.subscribe(nats_subject, cb=cache.message_handler)
        log.info(f"NATS, Subscribers, BinanceClient were starting")
        while True:
            for pair in COIN_PAIRS:
                try:
                    res = await get_pair_info(pair, client)
                    price = json.dumps(float(res["price"]))
                    try:
                        await nc.publish(
                            "update_price",
                            json.dumps({"pair": pair, "price": price}).encode(),
                        )
                        log.info("publisher_ok")
                    except Exception as exc:
                        log.error("publisher_bad", exc_info=exc)
                except Exception as e:
                    logger.error(f"Ошибка при обновлении цены для {pair}: {e}")

            await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Ошибка в основном цикле: {e}")
