import json

class Dataset_Definition:
    def __init__(self):
        self.__tables = []
        self.name = None

    def add_table(self, table_definition):
        self.__tables.append(table_definition)

    def json(self):
        return {
            'name': self.name if self.name else 'DefaultName',
            'tables': [table.json() for table in self.__tables]
        }

    def __str__(self):
        return json.dumps(self.json(), sort_keys=False, indent=4)
