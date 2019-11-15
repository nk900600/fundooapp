from locust import HttpLocust, TaskSet, between

header = {
    "Content-Type": 'application/json',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
                     ".eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTczODk0MjkyLCJqdGkiOiI1MzAzNTViYWU5Nzg0MWM1OWVmMWQxMWI4NzkxMmUyYSIsInVzZXJfaWQiOjF9.bXAAC45gOD-XSjwxf7iGw7IsfwQEjMj78Nh-jNbwdEo"}


def login(l):
    l.client.post("api/login/", {"username": "admin", "password": "admin"}, )


def logout(l):
    l.client.get("api/logout/", )


def forgotpassword(l):
    l.client.post("api/forgotpassword", {"email": "nk90600@gmail.com"})


def resetpassword(l):
    l.client.post("api/resetpassword/nk90600", {"password": "pankaj007"})


def noteget(l):
    l.client.get("api/notes/", headers=header, )


def notepost(l):
    l.client.post("api/notes/", {"title": "hi", "note": "hii"}, headers=header,)


def noteput(l):
    l.client.put("api/note/1", {"title": "hi", "note": "hii"}, headers=header,)


def notedel(l):
    l.client.delete("api/note/80", headers=header,)


def labelget(l):
    l.client.get("api/label", headers=header,)


def labelpost(l):
    l.client.post("api/label", {"name": "locust"}, headers=header)


def labelput(l):
    l.client.put("api/label/9", {"name": "locust"},headers=header,)


def labeldelete(l):
    l.client.delete("api/label/9", headers=header,)


def search(l):
    l.client.post("api/search", {"title": "ee"}, headers=header,)


def archive(l):
    l.client.get("api/archive",headers=header,)


def reminder(l):
    l.client.get("api/reminder",headers=header,)


def trash(l):
    l.client.get("api/trash", headers=header,)


class UserBehavior(TaskSet):
    tasks = {#noteget: 1,  notepost: 1, noteput: 1, notedel: 1, labelget: 1,
            labelpost: 1,}# labelput: 1, labeldelete: 1, trash: 1, archive: 1, reminder: 1,
             #search: 1, resetpassword: 1, forgotpassword: 1}

    # def on_start(self):
    #     login(self)

    # def on_stop(self):
    #     logout(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
