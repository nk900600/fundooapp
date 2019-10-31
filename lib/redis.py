import redis
from fundoo.settings import DB, PORT
# class function_wrapper(object):
#     def __init__(self, wrapped):
#         self.wrapped = wrapped
#     def __call__(self, *args, **kwargs):
#         return self.wrapped(*args, **kwargs)
red = redis.StrictRedis(host="localhost", db=DB, port=PORT)

#
# class Redis:
#
#     def set(self, key, value):
#         red.set(key, value)
#
#     def get(self, key):
#         red.get(key)
#
#     def delete(self, key):
#         red.delete(key)
#
#     def rpush(self, key,value):
#         red.rpush(key,value)
#
#     def hmset(self, key, value):
#         red.hmset(key, value)
#
#     def hget(self, key):
#         red.hget(key)