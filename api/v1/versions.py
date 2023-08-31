from itertools import chain
from flask_restful import Resource
from flask import request

from pylon.core.tools import log
from tools import api_tools


class ProjectAPI(api_tools.APIModeHandler):

    def get(self, project_id, prompt_name):
        return self.module.get_versions_by_prompt_name(project_id, prompt_name), 200

    def post(self, project_id):
        prompt_data = self.module.get_by_id(project_id, request.json['prompt_id'])
        prompt_data.pop('test_input')
        prompt_data.pop('tags')
        prompt_data.update({'version': request.json['version']})
        prompt = self.module.create(project_id, prompt_data)
        for i in chain(prompt_data['variables'], prompt_data['examples']):
            i['prompt_id'] = prompt['id']
        self.module.create_variables_bulk(project_id, prompt_data['variables'])
        self.module.create_examples_bulk(project_id, prompt_data['examples'])    
        return prompt, 201

class API(api_tools.APIBase):
    url_params = [
        '<string:mode>/<int:project_id>',
        '<int:project_id>',
        '<string:mode>/<int:project_id>/<string:prompt_name>',
        '<int:project_id>/<string:prompt_name>',
    ]

    mode_handlers = {
        'default': ProjectAPI,
    }