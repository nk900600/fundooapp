"""
 ******************************************************************************
 *  Purpose: purpose is to do load testing
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

from locust import HttpLocust, TaskSet


def login(user):
    """
    :param user: login function is created
    """
    user.client.post("/login/", {"username": "admin", "password": "admin"})


def index(user):
    """
    :param user: index function is created
    """
    user.client.get("/")


def note(user):
    """
    :param user: note function is created
    """
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
