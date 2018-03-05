class Dataset:

    UPDATE_POLICE_UPSERT = 'Upsert'

    def __init__(self, project, json):
        self.__project = project
        self.__json = json

    def load_table(self, table_definition, update_policy=UPDATE_POLICE_UPSERT):
        self.__project._request('PATCH',
                                     f'/datasets/{self.__json["datasetId"]}/tables/{table_definition.name}',
                                     headers={'updatePolicy':  update_policy},
                                     json=table_definition.json()
                                     )

    def __str__(self):
        return self.__json['name']
