from sqlalchemy import select, update, delete
from core.database import AsyncSessionLocal
from models.pairs import Pairs
import json
from core.logs import log


async def save_to_db(pair, price):
    try:
        price = price.replace('"', "")
        async with AsyncSessionLocal() as db:
            db_pair = await db.execute(select(Pairs).filter(Pairs.symbol == pair))
            result = db_pair.fetchone()
            if result is None:
                new_pair = Pairs(symbol=pair, price=float(price))
                db.add(new_pair)
                await db.commit()
                log.info(f"Added new pair: {pair} - {float(price)}")
            else:
                await db.execute(delete(Pairs).where(Pairs.symbol == pair))
                new_pair = Pairs(symbol=pair, price=float(price))
                db.add(new_pair)
                await db.commit()
                log.info(f"The pair: {pair} - {float(price)} has been updated")
            log.info("db_updated")
    except Exception as e:
        log.warning(
            f"The pair: {pair} - {float(price)} did not appear in the database!"
        )
        log.exception(e)


async def message_handler(msg):
    log.info(f"Message received: {msg}")
    log.info(f"Start saving to DB")
    json_data = msg.data.decode()
    data_dict = json.loads(json_data)
    await save_to_db(data_dict["pair"], data_dict["price"])
