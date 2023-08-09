from itertools import groupby

from flask import request, g
from pydantic import ValidationError
from pylon.core.tools import log

from tools import session_project, api_tools


class ProjectAPI(api_tools.APIModeHandler):

    def get(self, project_id: int, **kwargs):
        data = self.module.get_config(project_id=project_id, user_id=g.auth.id)

        data.integrations.append({
            'id': 23,
            'name': 'open_ai',
            'is_default': False,
            'config': {'name': 'openai1'}
        })

        data.integrations.append({
            'id': 2,
            'name': 'vertex_ai',
            'is_default': False,
            'config': {'name': 'vertex2'}
        })

        formatted_integrations = {
            str(k): list(v)
            for k, v in
            groupby(sorted(data.integrations, key=lambda x: x['name']), lambda x: x['name'])
        }

        try:
            selected_integration = next(i for i in data.integrations if i['is_default'])
        except StopIteration:
            selected_integration = data.integrations[0]

        table_data = [{'key': k, 'value': v} for k, v in data.dict(exclude={'integrations'}).items()]
        integrations_data = {'key': 'integrations', 'value': selected_integration['id'], 'action': formatted_integrations}
        table_data.append(integrations_data)
        return table_data, 200

    def put(self, project_id: int, **kwargs):
        # used to regenerate token from ui
        token = self.module.regenerate_token(user_id=g.auth.id)
        return {'token': token}, 200


# class AdminAPI(api_tools.APIModeHandler):
#     ...


class API(api_tools.APIBase):
    url_params = [
        '<string:mode>/<int:project_id>',
        '<int:project_id>',
    ]

    mode_handlers = {
        'default': ProjectAPI,
        # 'administration': AdminAPI,
    }