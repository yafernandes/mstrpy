from .dataset import Dataset
from .const import SEARCH_TYPE_EXACTLY, OBJECT_TYPE_REPORT_DEFINITION

class Project:
    def __init__(self, conn, json):
        self.__conn = conn
        self.__json = json
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

    def get_datasets(self, **kwargs):
        if 'id' in kwargs:
            r = self._request('GET',f'/datasets/{kwargs["id"]}')
            return Dataset(self, r.json())
        else:
            searchParams = {
                'limit': -1,
                'pattern': kwargs.get('search_type', SEARCH_TYPE_EXACTLY),
                'type': OBJECT_TYPE_REPORT_DEFINITION,
                'name': kwargs['name']
            }
        r = self._request('GET','/searches/results',params=searchParams)
        return [Dataset(self, dataset) for dataset in r.json()['result']]

    def __str__(self):
        return self.name
