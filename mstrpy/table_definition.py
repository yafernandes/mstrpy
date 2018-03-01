import base64
import json


class Table_Definition:
    def __init__(self):
        pass

    def name(self, name=None):
        if name:
            self._name = name
        return self._name

    def json(self):
        return {
            'name': self._name if self._name else 'DefaultName',
            'columnHeaders': self._columnHeaders if self._columnHeaders else 'DefaultColumnHeaders',
            'data': self._data if self._data else 'Default data'
        }

    def import_pandas(self, df):
        DATA_TYPE = {
            'object': 'STRING',
            'int64': 'INTEGER',
            'float64': 'DOUBLE',
            'bool': 'BOOL',
            'datetime64[ns]': 'DATETIME'
        }

        unsupported_types = {str(df[col].dtype)
                             for col in df if str(df[col].dtype) not in DATA_TYPE}
        if unsupported_types:
            raise Exception(
                f'Dataframe has unsupported data types: {unsupported_types}'
            )

        self._columnHeaders = [
            {'name': col,
             'dataType': DATA_TYPE[str(df[col].dtype)]
             } for col in df
        ]

        self._data = base64.b64encode(df.to_json(
            orient='records', date_format='iso').encode('utf-8')).decode('utf-8')

        return self

    def __str__(self):
        return json.dumps(self.json(), sort_keys=False, indent=4)
