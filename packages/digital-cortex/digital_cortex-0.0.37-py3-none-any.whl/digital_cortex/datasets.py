import requests

from digital_cortex.schema.datasets import *
from digital_cortex.schema.tags import TagForm

BASE_PATH = "/api/v1/datasets"


class Datasets:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def get_all_datasets_type(self):
        url = self.host_url + BASE_PATH + "/types"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_user_datasets(self):
        url = self.host_url + BASE_PATH
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_local_files(self):
        url = self.host_url + BASE_PATH + "/fileon/local"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_particular_dataset(self, dataset_id: str):
        url = self.host_url + BASE_PATH + f"/{dataset_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_user_and_published_datasets(self):
        url = self.host_url + BASE_PATH + "/userandpublished"
        response = requests.get(url, headers=self.headers).json()
        return response

    def create_remote_file_dataset(self, dataset_url_form: DatasetUrlForm):
        url = self.host_url + BASE_PATH + "/url/create"
        payload = dataset_url_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def create_cloud_file_dataset(self, dataset_cloud_file_form: DatasetCloudFileForm):
        url = self.host_url + BASE_PATH + "/file/cloud/create"
        payload = dataset_cloud_file_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def create_local_file_dataset(self, dataset_local_file_form: DatasetLocalFileForm, file_path: str):
        url = self.host_url + BASE_PATH + '/file/local/create'
        payload = {
            'datasetForm': dataset_local_file_form.model_dump_json(),
            'file': ('codeFile', open(file_path, 'rb'))
        }
        response = requests.post(url, headers=self.headers, files=payload)
        return response.text

    def create_database_dataset(self, database_dataset_form: DatabaseDatasetForm):
        url = self.host_url + BASE_PATH + '/database/create'
        payload = database_dataset_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def is_dataset_exists(self, name: str, dataset_id: str = None):
        if dataset_id is None:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}"
        else:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}&id={dataset_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def attach_tags_to_dataset(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/attachtags'
        payload = tag_form.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def detach_tags_from_dataset(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/detachtags'
        payload = tag_form.model_dump()
        response = requests.delete(url, headers=self.headers, json=payload)
        return response.text

    def get_all_published_datasets(self):
        url = self.host_url + BASE_PATH + "/published"
        response = requests.get(url, headers=self.headers).json()
        return response

    def publish_dataset(self, dataset_id: str):
        url = self.host_url + BASE_PATH + f"/{dataset_id}/publish"
        response = requests.put(url, headers=self.headers).json()
        return response

    def delete_dataset(self, dataset_id: str):
        url = self.host_url + BASE_PATH + f"/{dataset_id}/delete"
        response = requests.delete(url, headers=self.headers).json()
        return response

    def is_dataset_used_in_pipeline(self, dataset_id: str):
        url = self.host_url + BASE_PATH + f"/{dataset_id}/isusedinpipeline"
        response = requests.get(url, headers=self.headers).json()
        return response

    def update_remote_file_dataset(self, update_dataset_url_form: UpdateDatasetUrlForm):
        url = self.host_url + BASE_PATH + '/update/url'
        payload = update_dataset_url_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_cloud_file_dataset(self, update_dataset_cloud_file_form: UpdateDatasetCloudFileForm):
        url = self.host_url + BASE_PATH + '/update/file/cloud'
        payload = update_dataset_cloud_file_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_local_file_dataset(self, update_dataset_local_file_form: UpdateDatasetLocalFileForm):
        url = self.host_url + BASE_PATH + '/update/file/local'
        payload = update_dataset_local_file_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_database_dataset(self, update_database_dataset_form: UpdateDatabaseDatasetForm):
        url = self.host_url + BASE_PATH + '/update/database'
        payload = update_database_dataset_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_dataset_general_fields(self, update_general_fields_form: UpdateDatasetGeneralFieldsForm):
        url = self.host_url + BASE_PATH + '/update/generalfields'
        payload = update_general_fields_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_dataset_description(self, update_description_form: UpdateDatasetDescriptionForm):
        url = self.host_url + BASE_PATH + '/update/description'
        payload = update_description_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def validate_database(self, db_info: DBInfo):
        url = self.host_url + BASE_PATH + '/database/validate'
        payload = db_info.model_dump()
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def get_pending_actions(self, dataset_id: str):
        url = self.host_url + BASE_PATH + f"/{dataset_id}/pendingactions"
        response = requests.get(url, headers=self.headers).json()
        return response
