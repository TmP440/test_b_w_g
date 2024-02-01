import asyncio

host = "127.0.0.1"
user = "postgres"
password = "qwerty"
db_name = "test_b_w"
port = 5432
KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
KAFKA_TOPIC = "price_updates"
KAFKA_CONSUMER_GROUP = "group-id"
loop = asyncio.get_event_loop()
