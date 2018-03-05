import base64
import json


class Table_Definition:

    _DATA_TYPE = {
        'object': 'STRING',
        'int64': 'INTEGER',
        'float64': 'DOUBLE',
        'bool': 'BOOL',
        'datetime64[ns]': 'DATETIME'
    }

    def __init__(self):
        self.name = None

    def json(self):

        columnHeaders = [
            {'name': col,
             'dataType': Table_Definition._DATA_TYPE[str(self.__df[col].dtype)]
             } for col in self.__df
        ]

        data = base64.b64encode(self.__df.to_json(
            orient='records', date_format='iso').encode('utf-8')).decode('utf-8')

        return {
            'name': self.name if self.name else 'DefaultName',
            'columnHeaders': columnHeaders if columnHeaders else 'DefaultColumnHeaders',
            'data': data
        }

    def import_pandas(self, df, make_copy=False):
        unsupported_types = {str(df[col].dtype)
                             for col in df if str(df[col].dtype) not in Table_Definition._DATA_TYPE}
        if unsupported_types:
            raise Exception(
                f'Dataframe has unsupported data types: {unsupported_types}'
            )

        self.__df = df if not make_copy else df.copy()

        return self

    def __str__(self):
        return json.dumps(self.json(), sort_keys=False, indent=4)
