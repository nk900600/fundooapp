from locust import HttpLocust, TaskSet


def login(user):
    user.client.post("/login/", {"username": "admin", "password": "admin"})


def index(user):
    user.client.get("/")


def note(user):
    user.client.post("/note/", {"title": "hi", "note": ""})


class UserBehavior(TaskSet):
    tasks = {index: 2, note: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        note(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
