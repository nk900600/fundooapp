import json
import requests
from fundoo.settings import BASE_URL

with open("test.json") as f:
    data = json.load(f)


class TestCreate:
    """
    test case is created and test with predefined values
    """

    def test_create1(self):
        """
        test case is created for note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test1']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_create2(self):
        """
        test case is created for note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test2']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_create3(self):
        """
        test case is created for note and test with predefined values
        """
        url = BASE_URL + '/note/'
        file = data[0]['test3']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200


class TestNoteShare:
    """
    test case is created and test with predefined values
    """

    def test_NoteShare1(self):
        """
        test case is created for share note and test with predefined values
        """
        url = BASE_URL + '/noteshare/'
        file = data[0]['test4']
        response = requests.post(url=url, data=file)
        assert response.status_code == 404


if __name__ == '__main__':
    TestCreate()
    TestNoteShare()
