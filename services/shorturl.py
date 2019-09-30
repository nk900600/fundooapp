from bitly_api.bitly_api import Connection
import bitly_api

bit = "bf769ba8298c0206352ce6e073135c4d98e43fda"
b = bitly_api.Connection(access_token = bit)
response=b.shorten("http://127.0.0.1:8000/activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZiZ25nbmd2ZmIiLCJwYXNzd29yZCI6ImRmZCJ9.y_rwN40NOmhs6rShLrHbyH88NweD2WF8eRlwIYSoMm8/")
print(response)

