import typing

from core.database import get_db
from core.celery_app import app
from models.pairs import Pairs

celery_app = app


def save_to_db(pair, price):
    pass


@app.task()
def process_message(pair: str, price: str):
    try:
        with get_db() as db:
            print(1)
            db_pair = db.query(Pairs).filter_by(symbol=pair).first()
            print(2)
            if db_pair:
                print(2.2)
                db_pair.price = price
                print(2.3)
            else:
                print(3)
                db_pair = Pairs(symbol=pair, price=price)
                db.add(db_pair)
            db.commit()
    except Exception as ex:
        print("Не получилось сохранить данные")
        print(ex)
