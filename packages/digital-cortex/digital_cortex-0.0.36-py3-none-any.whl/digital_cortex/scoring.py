import requests

from digital_cortex.schema.scoring import *

BASE_PATH = "/api/v1/score"


class Scoring:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def text_score(self, text_scoring_form: TextScoringForm):
        url = self.host_url + BASE_PATH + '/text'
        payload = text_scoring_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text
