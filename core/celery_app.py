import celery

redis = "redis://127.0.0.1:6379/2"

app = celery.Celery("worker", broker=redis, backend=redis)

app.autodiscover_tasks(
    [
        "kafka_server.tasks.save_db"
    ],
    force=True,
)
