from locust import HttpUser, TaskSet, task
import random
import string
import json


class UserBehavior(TaskSet):

    def login(self):
        # Generate a random username and password
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Send a POST request to the login page with the username and password
        response = self.client.post("login/", {"username": username, "password": password})

        # Check if the login was successful
        if response.status_code == 200:
            # Return the generated username and password
            return username, password
        else:
            # If the login was not successful, raise an exception
            raise Exception("Failed to log in with username {} and password {}".format(username, password))

    @task
    def index(self):
        self.client.get("")

    @task
    def return_order(self):
        self.client.get("return_order/")

    @task
    def order_history(self):
        self.client.get("order_history/")

    @task
    def create_order(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.client.login(username=username, password=password)


        data = {
            'username': 'testuser1',
            'vehicle_type': 'Bike',
            'loc_id': '1'
        }
        response = self.client.post("create_order/", json.dumps(data),
                                    content_type='application/json')


    @task
    def deposit(self):
        self.client.get("deposit/")

    @task
    def payment(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.client.login(username=username, password=password)
        order_id = random.randint(1, 10)
        self.client.get("payment/{order_id}/")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 5000
    max_wait = 15000