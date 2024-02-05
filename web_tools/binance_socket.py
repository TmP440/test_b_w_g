import asyncio
import json
from core.logs import log
import websockets
from core import cache
from nats.aio.client import Client as NATSClient
from config import settings
from web_tools import getter_url
from tasks import save_db


async def on_message(message):
    log.info("Trying to get data from binance")
    if "s" in message and message["s"]:
        pair = message["s"]
        price = message["c"]
        await cache.set_value("exchanger", "binance")
        log.info(f"Binance returned the data")
        return pair, float(price)
    else:
        log.warning("Binance is not ok. Trying get data from CoinGeko.")
        message = await getter_url.get_data_from_coingeko()
        pair, price = message["pair"], float(message["price"])
        await cache.set_value("exchanger", "coingeko")
        log.info(f"Coingeko returned the data")
        return pair, price


async def exchange_usd_to_rub(pair, price, r_e_r):
    rub_pair = pair[:-4] + "RUB"
    rub_price = price * r_e_r
    return rub_pair, float(rub_price)


async def get_data_from_binance(stream_name: str):
    wss = f"{settings.wss_binance}{stream_name}"
    rub_exchange_rate = await getter_url.get_rub_exchange_rate()

    nc = NATSClient()
    await nc.connect(servers=[settings.nats_host + ":" + settings.nats_port])
    sub1 = await nc.subscribe(settings.nats_subject, cb=cache.message_handler)
    sub2 = await nc.subscribe(settings.nats_subject, cb=save_db.message_handler)
    log.info("NATS connecting")

    while True:
        try:
            async with websockets.connect(wss) as websocket:
                try:
                    rub_exchange_rate = await getter_url.get_rub_exchange_rate()
                except:
                    log.warning("Данные о курсе доллара не обновились.")
                data = await websocket.recv()
                message = json.loads(data)
                pair, price = await on_message(message)
                await nc.publish(
                    settings.nats_subject,
                    json.dumps({"pair": pair, "price": price}).encode(),
                )
                rub_pair, rub_price = await exchange_usd_to_rub(
                    pair, price, rub_exchange_rate
                )
                await nc.publish(
                    settings.nats_subject,
                    json.dumps({"pair": rub_pair, "price": rub_price}).encode(),
                )
        except websockets.exceptions.ConnectionClosed:
            log.warning("Binance WebSocket connection failed")


async def update_info():
    pairs = [f"{symbol}@ticker" for symbol in settings.coin_pairs]

    await asyncio.gather(get_data_from_binance("/".join(pairs)))
