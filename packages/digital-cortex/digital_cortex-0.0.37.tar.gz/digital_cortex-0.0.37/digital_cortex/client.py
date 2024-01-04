from digital_cortex.config import config
from digital_cortex.datasets import Datasets
from digital_cortex.functions import Functions
from digital_cortex.models import Models
from digital_cortex.pipelines import Pipelines
from digital_cortex.scoring import Scoring
from digital_cortex.tags import Tags

# HOST_URL = config.HOST_URL

# BASE_PATH = '/api/v1/functions'


class DigitalCortex(Models, Functions, Datasets, Pipelines, Scoring, Tags):
    def __init__(self, token):
        self.token = token
        self.host_url = config.HOST_URL
        self.headers = {'Authorization': f'Bearer {token}'}
        super().__init__(self.host_url, self.headers)


def client(token):
    return DigitalCortex(token)
