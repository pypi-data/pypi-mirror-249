import functools
import inspect
import json
import re

import requests

from digital_cortex.function_creator import FunctionCreator
from digital_cortex.function_runner import FunctionRunner
from digital_cortex.schema.functions import *
from digital_cortex.schema.tags import TagForm

BASE_PATH = "/api/v1/functions"


class Functions:
    def __init__(self, host_url, headers):
        self.host_url = host_url
        self.headers = headers

    def get_all_function_compute_types(self):
        url = self.host_url + BASE_PATH + "/computetypes"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_all_user_functions(self):
        url = self.host_url + BASE_PATH
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_particular_function(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}"
        response = requests.get(url, headers=self.headers).json()
        res = json.dumps(response, indent=2)
        return re.sub(r"\\n", "\n", res)

    def get_all_published_function(self):
        url = self.host_url + BASE_PATH + "/published"
        response = requests.get(url, headers=self.headers).json()
        return response

    def get_user_and_published_function(self):
        url = self.host_url + BASE_PATH + "/userandpublished"
        response = requests.get(url, headers=self.headers).json()
        return response

    def update_code(self, update_function_code_form: UpdateFunctionCodeForm):
        url = self.host_url + BASE_PATH + "/update/code"
        payload = dict(update_function_code_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_code_file(self, function_id: str, code_file_path: str):
        url = self.host_url + BASE_PATH + "/update/codefile"
        payload = {
            'id': function_id,
            'codeFile': ('codeFile', open(code_file_path, 'rb'))
        }
        response = requests.put(url, headers=self.headers, files=payload)
        return response.text

    def update_function_dependency(self, update_dependency_form: UpdateFunctionDependencyForm,
                                   dependency_file_path: str = None):
        url = self.host_url + BASE_PATH + '/update/dependency'
        payload = {
            'updateDependencyForm': update_dependency_form.model_dump_json()
        }

        if dependency_file_path:
            payload['dependencyFile'] = ('dependencyFile', open(dependency_file_path, 'rb'))
        response = requests.put(url, headers=self.headers, files=payload)
        return response.text

    def update_function_description(self, update_description_form: UpdateFunctionDescriptionForm):
        url = self.host_url + BASE_PATH + '/update/description'
        payload = dict(update_description_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def update_function_general_fields(self, update_general_fields_form: UpdateFunctionGeneralFieldsForm):
        url = self.host_url + BASE_PATH + '/update/generalfields'
        payload = dict(update_general_fields_form)
        response = requests.put(url, headers=self.headers, json=payload)
        return response.text

    def attach_tags_to_function(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/attachtags'
        payload = dict(tag_form)
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def detach_tags_from_functions(self, tag_form: TagForm):
        url = self.host_url + BASE_PATH + '/detachtags'
        payload = dict(tag_form)
        response = requests.delete(url, headers=self.headers, json=payload)
        return response.text

    def get_function_pending_actions(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}/pendingactions"
        response = requests.get(url, headers=self.headers).json()
        return response

    def publish_function(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}/publish"
        response = requests.put(url, headers=self.headers).json()
        return response

    def remove_function_dependency(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}/removedependency"
        response = requests.delete(url, headers=self.headers).json()
        return response

    def delete_function(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}/delete"
        response = requests.delete(url, headers=self.headers).json()
        return response

    def is_function_used_in_pipeline(self, function_id: str):
        url = self.host_url + BASE_PATH + f"/{function_id}/isusedinpipeline"
        response = requests.get(url, headers=self.headers).json()
        return response

    def is_function_exists(self, name: str, function_id: str = None):
        if function_id is None:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}"
        else:
            url = self.host_url + BASE_PATH + f"/isexists?name={name}&id={function_id}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def evaluate_function(self, payload: dict):
        url = self.host_url + BASE_PATH + "/evaluate/script"
        response = requests.post(url, headers=self.headers, json=payload)
        return response.text

    def cortexone(
            self,
            compute_type,
            run=True,
            create_or_update=False,
            blocking=False,
            delete=False,
            is_published=False,
            dependencies=[],
            geography='*',
            **kwargs
    ):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                full_source = inspect.getsource(func)
                # Find the line number where the inner function code starts
                inner_function_name = func.__name__
                start_line = full_source.index(inner_function_name)
                # Extract and print the source code of the inner function
                inner_function_code = full_source[start_line:]
                code = f"def {inner_function_code}"

                if run == True:
                    payload = {"computeType": compute_type, "script": code,
                               "dependency": dependencies, "params": {"args": args, "kwargs": kwargs},
                               "functionName": inner_function_name,
                               "async": blocking, "createOrUpdate": create_or_update, "isPublished": is_published,
                               "geography": geography}
                    url = self.host_url + BASE_PATH + "/sdk/evaluate/script"
                    response = requests.post(url, headers=self.headers, json=payload)
                    result = response.text

                else:
                    result = None

                return result

            return wrapper

        return decorator

    def get_function(self, function_id):
        return FunctionRunner(self.host_url, self.headers, function_id)

    def create_function(self, function_name, compute_type: str, dependencies=[], create_or_update: bool = False,
                        blocking: bool = False,
                        is_published: bool = False):
        script = inspect.getsource(function_name)
        return FunctionCreator(host_url=self.host_url, headers=self.headers, compute_type=compute_type,
                               name=function_name.__name__,
                               script=script, dependencies=dependencies, create_or_update=create_or_update,
                               blocking=blocking,
                               is_published=is_published)
