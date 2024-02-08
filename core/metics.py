from datetime import datetime
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import Point, WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from config import settings
from core.logs import log


async def save_status_code_in_influxdb(request, status_code):
    async with InfluxDBClientAsync(
        url=f"http://{settings.influx_settings['host']}:{settings.influx_settings['port']}",
        token=settings.influx_token,
        org=settings.influx_settings["org_name"],
    ) as client:
        try:
            write_api = client.write_api()

            point = (
                Point("http_requests")
                .tag("method", request)
                .time(datetime.utcnow(), WritePrecision.MS)
                .field("status_code", status_code)
            )

            successfully = await write_api.write(
                bucket=settings.influx_settings["bucket"], record=[point]
            )
            log.debug(f"{successfully}")
            log.info(f"Status code saved to InfluxDB: {status_code}")
        except InfluxDBError as e:
            log.error(f"Fail saved status code in influxdb: {e}")
