import asyncio
import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
from core.database import get_db
from models.pairs import Pairs
from config import loop, KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP


async def save_to_db(pair, price):
    async with get_db() as db:
        db_pair = db.query(Pairs).filter_by(symbol=pair).first()
        if db_pair:
            db_pair.price = price
        await db.commit()


async def process_message():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BROKER,
                                group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode())
            pair = data["pair"]
            price = data["price"]

            asyncio.run(save_to_db(pair, price))
    except Exception as ex:
        print(ex)
