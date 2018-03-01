import json


class Dataset_Definition:
    def __init__(self):
        self._tables = []
        pass

    def name(self, name=None):
        if name:
            self._name = name
        return self._name

    def add_table(self, table_definition):
        self._tables.append(table_definition)

    def json(self):
        return {
            'name': self._name if self._name else 'DefaultName',
            'tables': [table.json() for table in self._tables]
        }

    def __str__(self):
        return json.dumps(self.json(), sort_keys=False, indent=4)
