import bitly_api
# import bitly_api
#
# bit = "bf769ba8298c0206352ce6e073135c4d98e43fda"
# b = bitly_api.Connection(access_token = bit)
# response=b.shorten(uri="http://127.0.0.1:8000/activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZiZ25nbmd2ZmIiLCJwYXNzd29yZCI6ImRmZCJ9.y_rwN40NOmhs6rShLrHbyH88NweD2WF8eRlwIYSoMm8/")
# print(response)

# brightness_4


API_USER = "o_5lvqr5os3u"
API_KEY = "R_ced497e6748847e8a178067255870925"

b = bitly_api.Connection(API_USER, API_KEY)

# Replace this with your Long URL Here
longurl = "http://127.0.0.1:8000/activate/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImZiZ25nbmd2ZmIiLCJwYXNzd29yZCI6ImRmZCJ9.y_rwN40NOmhs6rShLrHbyH88NweD2WF8eRlwIYSoMm8/"
response = b.shorten(uri=longurl)

# Now let us print the Bitly URL
# print(response)
