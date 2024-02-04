from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_exchanges(self):
        self.client.get(url="/api/v1/exchange")

    @task
    def exchange(self):
        self.client.get(url="/api/v1/exchange?symbol=BTCUSDT")
