pg_host = "postgres-docker"
pg_user = "postgres"
pg_password = "qwerty"
db_name = "test_b_w"
pg_port = 5432
convert_pairs_to_CG_syntax = {
    "BTCUSDT": {"id": "bitcoin", "currencies": "usd"},
    "BTCRUB": {"id": "bitcoin", "currencies": "rub"},
    "ETHUSDT": {"id": "ethereum", "currencies": "usd"},
    "ETHRUB": {"id": "ethereum", "currencies": "rub"},
    "USDTTRCUSDT": {"id": "tether", "currencies": "usd"},
    "USDTTRCRUB": {"id": "tether", "currencies": "rub"},
    "USDTERCUSDT": {"id": "tether", "currencies": "usd"},
    "USDTERCRUB": {"id": "tether", "currencies": "rub"},
}
COIN_PAIRS = [
    "BTCUSDT",
    "BTCRUB",
    "ETHUSDT",
    "ETHRUB",
    "USDTTRCUSDT",
    "USDTTRCRUB",
    "USDTERCUSDT",
    "USDTERCRUB",
]
API_KEY = "j4R4t82xbWMl1DYVViKTcQV72T6ncll2AThtxW5P5PbsWNjsuJDEzdsCWYbURu4B"
SECRET_KEY = "8lTDhpCsmYH3xzXlgXhDMFaU7lzDNPJpt9Jzv71y3plMCgLEoSceiRYR6ycqjgaq"
nats_subject = "update_price"
nats_host = "nats://nats-docker"
nats_port = "4222"
redis_host = "redis-docker"
redis_port = "6379"
