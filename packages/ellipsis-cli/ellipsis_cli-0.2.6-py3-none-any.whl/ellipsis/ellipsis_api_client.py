from logging import Logger
from typing import Optional
from requests import Response, request


logger = Logger(__name__)



class EllipsisApiClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.health_check()

    def health_check(self):
        response: Response = self._request('GET', '/internal/health')
        response.raise_for_status()

    def register_codespace(self, name: str, repository_owner_login: str, repository_name: str, access_token: str, user: str):
        response: Response = self._request(
            'POST',
            '/workspaces/codespaces',
            json = {
                "name": name,
                "repository_owner_login": repository_owner_login,
                "repository_name": repository_name,
                "access_token": access_token,
                "user": user
            }
        )
        response.raise_for_status()
        return
    
    def register_internal_ec2_workspace(self, workspace_id: str, host_name: str, workflow_id: str):
        response: Response = self._request(
            'POST',
            '/workspaces',
            json = {
                "workspace_id": workspace_id,
                "workflow_id": workflow_id,
                "host_name": host_name, 
            }
        )
        response.raise_for_status()
        return

    def _request(self, method: str, path: str, **kwargs) -> Response:
        logger.debug(f'EllipsisApiClient request: {method} {path} {kwargs}')
        resp: Response = request(
            method,
            self.base_url + path,
            **kwargs
        )
        logger.debug(f'EllipsisApiClient response: {resp.status_code} {resp.text}')
        return resp
