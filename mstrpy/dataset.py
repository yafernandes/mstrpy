from mstrpy import UPDATE_POLICE_UPSERT

class Dataset():

    def __init__(self, project, json):
        self.__project = project
        self.__json = json
        self.name = json['name']
        self.id = json['id']

    def load_table(self, table_definition, update_policy=UPDATE_POLICE_UPSERT):
        self.__project._request('PATCH',
                                     f'/datasets/{self.id}/tables/{table_definition.name}',
                                     headers={'updatePolicy':  update_policy},
                                     json=table_definition.json()
                                     )

    def __str__(self):
        return self.name
