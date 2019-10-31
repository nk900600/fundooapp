import json
import requests
from fundoo.settings import BASE_URL, TEST_TOKEN

with open("test.json") as f:
    data = json.load(f)
headers = {
            'Content_Type': "application/json",
            'Authorization': TEST_TOKEN
}


class TestLogin:
    """
    test case is created and test with predefined values
    """
    def test_login(self):
        url = BASE_URL + '/login/'
        file = data[0]['test14']
        response = requests.post(url=url, data=file)
        assert response.status_code == 201


class TestNote:
    """
    test case is created and test with predefined values
    """

    def test_note1_post(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test5']
        response = requests.post(url=url, data=file,headers=headers)
        assert response.status_code == 201

    def test_note2_post(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test6']
        response = requests.post(url=url, data=file,headers=headers)
        assert response.status_code == 400

    def test_note3_post(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test7']
        response = requests.post(url=url, data=file,headers=headers)
        print(response.text)
        assert response.status_code == 201

    def test_note1_get(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/'+(data[0]['test11']['note_name'])
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 404

    def test_note2_get(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test12']['note_name'])
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 404

    def test_note3_get(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test13']['note_name'])
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200

    def test_note1_delete(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test13']['note_name'])
        response = requests.delete(url=url, headers=headers)
        assert response.status_code == 201

    def test_note2_delete(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test12']['note_name'])
        response = requests.delete(url=url, headers=headers)
        assert response.status_code == 400

    def test_note3_delete(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test11']['note_name'])
        response = requests.delete(url=url, headers=headers)
        assert response.status_code == 400

    def test_note1_put(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test13']['note_name'])
        data1= data[0]['test5']
        response = requests.put(url=url,data=data1, headers=headers)
        assert response.status_code == 200

    def test_note2_put(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test12']['note_name'])
        data1 = data[0]['test5']
        response = requests.put(url=url, data=data1, headers=headers)
        assert response.status_code == 404

    def test_note3_put(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/note/' + (data[0]['test11']['note_name'])
        data1 = data[0]['test5']
        response = requests.put(url=url, data=data1, headers=headers)
        assert response.status_code == 404


class TestLabelPut:

    def test_label_put1(self):
        """
        test case is created for share note and test with predefined values
        """

        url = BASE_URL + '/label/6'
        data1 = data[0]['test8']
        response = requests.put(url=url, data=data1, headers=headers)
        print(response.text)
        assert response.status_code == 200

    def test_label_put2(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label/' + data[0]['test9']['note_name']
        file = data[0]['test9']
        response = requests.put(url=url, data=json.dumps(file), headers=headers)
        print(response.text)
        assert response.status_code == 404

    def test_label_put3(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label/5'
        file = data[0]['test10']
        response = requests.put(url=url, data=file, headers=headers)
        assert response.status_code == 200

    def test_label_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label'
        response = requests.get(url=url,  headers=headers)
        assert response.status_code == 200

    def test_label_get2(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/label' + str(data[0]['test13']['note_name'])
        response = requests.get(url=url,  headers=headers)
        assert response.status_code == 404


class TestRemainder:
    def test_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/reminder'
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200

#
class TestArchive:
    def test_get1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/archive'
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200
