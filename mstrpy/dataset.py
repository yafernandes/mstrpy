class Dataset:

    UPDATE_POLICE_UPSERT = 'Upsert'

    def __init__(self, project, json):
        self._project = project
        self._json = json

    def load_table(self, table_definition, update_policy=UPDATE_POLICE_UPSERT):
        self._project._conn._request('PATCH',
                                     f'/datasets/{self._json["datasetId"]}/tables/{table_definition.name()}',
                                     headers={**self._project._headers, **
                                              {'updatePolicy':  update_policy}},
                                     json=table_definition.json()
                                     )

    def __str__(self):
        return self._json['name']
