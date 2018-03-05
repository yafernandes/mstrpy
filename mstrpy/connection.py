import json
import logging

import requests

from .project import Project


class Connection:

    __log = logging.getLogger('MicroStrategy REST API')
    __log.setLevel(logging.INFO)

    def __init__(self, config):
        self.__config = config
        self.__baseURL = 'https://{}:{}/{}/api'.format(self.__config['REST_server']['host'],
                                                      self.__config['REST_server']['port'],
                                                      self.__config['REST_server']['web_application'])
        self._session = requests.Session()

    def connect(self):
        r = self._request('POST',
                          self.__baseURL + '/auth/login',
                          json=self.__config['REST_server']['credential'])

        self._session.headers.update(
            {'X-MSTR-AuthToken': r.headers['X-MSTR-AuthToken']}
        )
        return self

    def _request(self, method, path, headers={}, json=None, params={}):
        r = self._session.request(method,
                                  self.__baseURL + path,
                                  params=params,
                                  headers=headers,
                                  json=json
                                  )

        if r.ok:
            return r
        else:
            Connection.__log.error(
                f'HTTP call failed with error code {r.status_code}')
            Connection.__log.error(f'Error message is {r.content}')
            Connection.__log.debug(r)
            raise Exception(r.content)

    def projects(self):
        projects = self._request('GET', '/projects')
        for project in projects.json():
            yield Project(self, project)

    def get_project(self, project_name):
        for project in self.projects():
            if project.name == project_name:
                return project

    def __str__(self):
        return self.__baseURL
