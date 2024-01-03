import requests

from digital_cortex.schema.pipelines import *
from digital_cortex.schema.tags import TagForm

BASE_PATH = "/api/v1/pipelines"


class Pipelines:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def get_all_pipeline_types(self):
        url = self.host_url + BASE_PATH + "/types"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_user_pipelines(self):
        url = self.host_url + BASE_PATH
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_particular_pipeline(self, pipeline_id: str):
        url = self.host_url + BASE_PATH + f"/{pipeline_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def create_etl_pipeline(self, etl_pipeline_form: EtlPipelineForm):
        url = self.host_url + BASE_PATH + '/etl/create'
        payload = etl_pipeline_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def update_etl_pipeline(self, update_etl_pipeline_form: UpdateEtlPipelineForm):
        url = self.host_url + BASE_PATH + '/etl/update'
        payload = update_etl_pipeline_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def is_pipeline_exists(self, name: str, pipeline_id: str = None):
        if pipeline_id is None:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}"
        else:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}&id={pipeline_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def attach_tags_to_pipeline(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/attachtags'
        payload = tag_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def detach_tags_from_pipeline(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/detachtags'
        payload = tag_form.model_dump()
        response = requests.delete(url, headers=self.headers, json=payload)
        return response.text

    def publish_pipeline(self, pipeline_id: str):
        url = self.host_url + BASE_PATH + f"/{pipeline_id}/publish"
        response = requests.put(url, headers=self.headers).json()
        return response

    def get_all_published_pipelines(self):
        url = self.host_url + BASE_PATH + "/published"
        response = requests.get(url, headers=self.headers).json()
        return response

    def update_pipeline_description(self, update_description_form: UpdatePipelineDescriptionForm):
        url = self.host_url + BASE_PATH + '/update/description'
        payload = update_description_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_pipeline_general_fields(self, update_general_fields_form: UpdatePipelineGeneralFieldsForm):
        url = self.host_url + BASE_PATH + '/update/generalfields'
        payload = update_general_fields_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def get_pipeline_pending_actions(self, pipeline_id: str):
        url = self.host_url + BASE_PATH + f"/{pipeline_id}/pendingactions"
        response = requests.get(url, headers=self.headers).json()
        return response

    def delete_pipeline(self, pipeline_id: str):
        url = self.host_url + BASE_PATH + f"/{pipeline_id}/delete"
        response = requests.delete(url, headers=self.headers).json()
        return response
