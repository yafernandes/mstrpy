from .dataset import Dataset
from .const import SEARCH_TYPE_EXACTLY, OBJECT_TYPE_REPORT_DEFINITION


class Project:
    def __init__(self, conn, json):
        self.__conn = conn
        self.__headers = {'X-MSTR-ProjectID': json['id']}

    def _request(self, method, path, headers={}, json=None, params={}):
        return self.__conn._request(method,
                                  path,
                                  params=params,
                                  headers={**self.__headers, **headers},
                                  json=json
                                  )

    @property
    def name(self):
        return self.__json['name']

    @name.setter
    def name(self, value):
        raise Exception('Unsupported operation')

    def create_dataset(self, dataset_definition):
        r = self._request('POST',
                                '/datasets',
                                headers=self.__headers,
                                json=dataset_definition.json())
        return Dataset(self, r.json())

    def get_datasets(self, name, search_type = SEARCH_TYPE_EXACTLY):
        searchParams = {
            'limit': -1,
            'pattern': search_type,
            'type': OBJECT_TYPE_REPORT_DEFINITION,
            'name': name
        }
        r = self._request('GET','/searches/results',params=searchParams)
        return [Dataset(self, dataset) for dataset in r.json()['result']]

    def __str__(self):
        return self.name
