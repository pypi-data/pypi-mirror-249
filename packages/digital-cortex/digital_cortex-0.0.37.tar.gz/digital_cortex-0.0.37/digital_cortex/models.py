import requests

from digital_cortex.schema.models import *
from digital_cortex.schema.tags import TagForm

BASE_PATH = "/api/v1/models"


class Models:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def get_all_base_models(self):
        url = self.host_url + "/api/v1/basemodels"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_models_tasks(self):
        url = self.host_url + "/api/v1/tasks"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_user_models(self):
        url = self.host_url + BASE_PATH
        response = requests.get(url, headers=self.headers).json()
        return response

    def is_model_exists(self, name: str, model_id: str = None):
        if model_id is None:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}"
        else:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}&id={model_id}"

        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_published_models(self):
        url = self.host_url + BASE_PATH + "/published"
        response = requests.get(url, headers=self.headers).json()
        return response

    def publish_model(self, model_id: str):
        url = self.host_url + BASE_PATH + f"/{model_id}/publish"
        response = requests.put(url, headers=self.headers).json()
        return response

    def get_particular_model(self, model_id: str):
        url = self.host_url + BASE_PATH + f"/{model_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_user_and_published_models(self):
        url = self.host_url + BASE_PATH + "/userandpublished"
        response = requests.get(url, headers=self.headers).json()
        return response

    def update_model_attached_tasks(self, update_task_form: UpdateTaskForm):
        url = self.host_url + BASE_PATH + '/update/tasks'
        payload = dict(update_task_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_model_general_fields(self, update_general_fields_form: UpdateModelGeneralFieldsForm):
        url = self.host_url + BASE_PATH + '/update/generalfields'
        payload = dict(update_general_fields_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_model_description(self, update_description_form: UpdateModelDescriptionForm):
        url = self.host_url + BASE_PATH + '/update/description'
        payload = dict(update_description_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def get_model_pending_actions(self, model_id: str):
        url = self.host_url + BASE_PATH + f"/{model_id}/pendingactions"
        response = requests.get(url, headers=self.headers).json()
        return response

    def attach_tags_to_model(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/attachtags'
        payload = dict(tag_form)
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def detach_tags_from_model(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/detachtags'
        payload = dict(tag_form)
        response = requests.delete(url, headers=self.headers, json=payload)
        return response.text

    def create_regex_model(self, regex_model_form: RegexModelForm, file_path: str):
        url = self.host_url + BASE_PATH + '/regex/import'
        payload = {
            'modelForm': regex_model_form.model_dump_json(),
            'file': ('file', open(file_path, 'rb'))

        }
        response = requests.post(url, headers=self.headers, files=payload)
        return response.text

    def create_pytorch_model(self, pytorch_model_form: PyTorchModelForm, file_path: str):
        url = self.host_url + BASE_PATH + '/pytorch/create'
        payload = {
            'modelForm': pytorch_model_form.model_dump_json(),
            'file': ('file', open(file_path, 'rb'))
        }
        response = requests.post(url, headers=self.headers, files=payload)
        return response.text

    def update_pytorch_model(self, update_pytorch_model_form: UpdatePytorchModelForm):
        url = self.host_url + BASE_PATH + '/pytorch/update'
        payload = update_pytorch_model_form.model_dump()
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def create_trained_model(self, create_trained_model_form: TrainedModelForm):
        url = self.host_url + BASE_PATH + '/trainedmodel/create'
        payload = dict(create_trained_model_form)
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def update_trained_model(self, update_trained_model_form: UpdateTrainedModelForm):
        url = self.host_url + BASE_PATH + '/trainedmodel/update'
        payload = dict(update_trained_model_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def get_trained_and_base_models(self):
        url = self.host_url + BASE_PATH + '/trainedandbasemodels'
        response = requests.get(url, headers=self.headers)
        return response.text

    def delete_model(self, model_id: str):
        url = self.host_url + BASE_PATH + f"/{model_id}/delete"
        response = requests.delete(url, headers=self.headers).json()
        return response

    def is_used_in_pipeline(self, model_id: str):
        url = self.host_url + BASE_PATH + f"/{model_id}/isusedinpipeline"
        response = requests.get(url, headers=self.headers).json()
        return response
