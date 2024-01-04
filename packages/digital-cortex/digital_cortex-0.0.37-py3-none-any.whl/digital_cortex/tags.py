import requests

BASE_PATH = "/api/v1/tags"


class Tags:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def get_all_tags(self):
        url = self.host_url + BASE_PATH
        response = requests.get(url, headers=self.headers).json()
        return response

    def create_tag(self, tag_name: str):
        url = self.host_url + BASE_PATH + f"/create?name={tag_name}"
        response = requests.post(url, headers=self.headers).json()
        return response

    def is_tag_exists(self, name: str, tag_id: str = None):
        if tag_id is None:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}"
        else:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}&id={tag_id}"
        response = requests.get(url, headers=self.headers).json()
        return response
