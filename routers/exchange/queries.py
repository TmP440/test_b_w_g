from models.pairs import Pairs
from sqlalchemy import select
from core.database import AsyncSessionLocal


async def get_all_pairs(symbol: str):
    async with AsyncSessionLocal() as db:
        db_pairs = await db.execute(select(Pairs))
        return db_pairs.fetchall()
