import json
import requests
from fundoo.settings import BASE_URL

with open("test.json") as f:
    data = json.load(f)
headers={
            'Content_Type':"application/json",
            'Authorization':"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTcxODA2NzQwLCJqdGkiOiIxNzYyY2E4NWNkZTE0Y2QzODNhMmNlOWE1ZjJiOWE5OSIsInVzZXJfaWQiOjF9.qVRlawT0RGbg8TY6Wci_vj8g_unVoRADVbOhDcIJrbA"
        }


class TestLabel:
    """
    test case is created and test with predefined values
    """

    def test_label1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test5']
        # print(json.dumps(file), type(json.dumps(file)))
        response = requests.post(url=url, data=file,headers=headers)
        print(response.text)
        assert response.status_code == 400
#
#     def test_label2(self):
#         """
#         test case is created for share note and test with predefined values
#         """
#         url = BASE_URL + '/note/'
#         file = data[0]['test6']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 200
#
#     def test_label3(self):
#         """
#         test case is created for share note and test with predefined values
#         """
#         url = BASE_URL + '/note/'
#         file = data[0]['test7']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 200
#

class TestLabelPut:

    def test_login(self):
        url = BASE_URL + '/login/'
        file = data[0]['test14']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200


    def test_put1(self):
        """
        test case is created for share note and test with predefined values
        """

        url = BASE_URL + '/label/' + data[0]['test8']['note_name']
        data1 = data[0]['test8']
        response = requests.put(url=url, data=json.dumps(data1), headers=headers)
        assert response.status_code == 200

    def test_put2(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label/' + data[0]['test9']['note_name']
        file = data[0]['test9']
        response = requests.put(url=url, data=json.dumps(file), headers=headers)
        assert response.status_code == 404

    def test_put3(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label/' + data[0]['test10']['note_name']
        file = data[0]['test10']
        response = requests.put(url=url, data=json.dumps(file), headers=headers)
        assert response.status_code == 200


class TestLabelGet:
    def test_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label'
        response = requests.get(url=url,  headers=headers)
        assert response.status_code == 200

    def test_get2(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label/' + data[0]['test13']['note_name']
        response = requests.get(url=url,  headers=headers)
        assert response.status_code == 405


class TestRemainder:
    def test_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/reminder'
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200


class TestArchive:
    def test_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/archive'
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200
