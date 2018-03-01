from .dataset import Dataset


class Project:
    def __init__(self, conn, json):
        self._conn = conn
        self._json = json
        self._headers = {'X-MSTR-ProjectID': json['id']}

    def name(self):
        return self._json['name']

    def create_dataset(self, dataset_definition):
        r = self._conn._request('POST',
                                '/datasets',
                                headers=self._headers,
                                json=dataset_definition.json())
        return Dataset(self, r.json())

    def __str__(self):
        return self.name()
