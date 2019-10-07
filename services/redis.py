import redis
from fundoo.settings import DB, PORT
red = redis.StrictRedis(host="localhost", db=DB, port=PORT)


class Redis:

    def set(self, key, value):
        red.set(key, value)

    def get(self, key):
        red.get(key)

    def delete(self, key):
        red.delete(key)
