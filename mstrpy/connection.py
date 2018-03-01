import json
import logging

import requests

from .project import Project


class Connection:

    _log = logging.getLogger('MicroStrategy REST API')
    _log.setLevel(logging.INFO)

    def __init__(self, config):
        self._config = config
        self._baseURL = 'https://{}:{}/{}/api'.format(self._config['REST_server']['host'],
                                                      self._config['REST_server']['port'],
                                                      self._config['REST_server']['web_application'])
        self._session = requests.Session()

    def connect(self):
        r = self._request('POST',
                          self._baseURL + '/auth/login',
                          json=self._config['REST_server']['credential'])

        self._session.headers.update(
            {'X-MSTR-AuthToken': r.headers['X-MSTR-AuthToken']}
        )
        return self

    def _request(self, method, path, headers={}, json=None):
        r = self._session.request(method,
                                  self._baseURL + path,
                                  headers=headers,
                                  json=json
                                  )

        if r.ok:
            return r
        else:
            Connection._log.error(
                f'HTTP call failed with error code {r.status_code}')
            Connection._log.error(f'Error message is {r.content}')
            Connection._log.debug(r)
            raise Exception(r.content)

    def projects(self):
        projects = self._request('GET', '/projects')
        for project in projects.json():
            yield Project(self, project)

    def get_project(self, project_name):
        for project in self.projects():
            if project.name() == project_name:
                return project

    def __str__(self):
        return self._baseURL
