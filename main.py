import uvicorn
import asyncio
from threading import Thread  # Пока забить
from aiomultiprocess import Process
from binance_async import binance_api
from fastapi import FastAPI
from routers.exchange import exchange_router_v1

app = FastAPI()
app.include_router(exchange_router_v1, prefix="/api/v1", tags=["exchange"])


async def run_uvicorn():
    await uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, workers=3)


async def run_tasks():
    uvicorn_process = Process(target=run_uvicorn)
    uvicorn_process.start()

    await binance_api.update_info()

    uvicorn_process.join()


if __name__ == "__main__":
    asyncio.run(run_tasks())
