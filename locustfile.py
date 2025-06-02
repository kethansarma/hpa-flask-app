from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(2, 5)
        
    @task
    def about(self):
        self.client.get("/")
    @task
    def about(self):
        self.client.get("/logs")