import uvicorn
import asyncio
from aiomultiprocess import Process
from nats_server.producer_binance import binance_api
from fastapi import FastAPI
from routers.exchange.exchange import exchange_router_v1

app = FastAPI()
app.include_router(exchange_router_v1, prefix="/api/v1", tags=["exchange"])


async def run_uvicorn():
    await uvicorn.run("main:app", host="0.0.0.0", port=5051, reload=True, workers=10)


async def run_tasks():
    uvicorn_process = Process(target=run_uvicorn)
    uvicorn_process.start()

    await binance_api.update_info()

    uvicorn_process.join()


if __name__ == "__main__":
    asyncio.run(run_tasks())
