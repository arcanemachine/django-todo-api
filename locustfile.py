import os

from locust import HttpUser, task

host = os.environ.get("PROJECT_HOST", "http://localhost:8000")


# locust --web-host=0.0.0.0 --host=$PROJECT_HOST
class ApiRootSwarm(HttpUser):
    endpoint = f"{host}/api"

    @task
    def get(self):
        self.client.get(self.endpoint)

    @task
    def head(self):
        self.client.head(self.endpoint)

    @task
    def options(self):
        self.client.options(self.endpoint)
