import base64
import copy
import datetime
import json
import logging
import os
import ssl

import pandas as pd
import requests

from mstrpy import Connection, Dataset_Definition, Table_Definition, SEARCH_TYPE_BEGIN_WITH


def pandas_sample():

    ssl._create_default_https_context = ssl._create_unverified_context

    link = 'http://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/ufo.csv'
    df = pd.read_csv(link)

    td = Table_Definition()
    td.name = 'SampleTable'
    td.import_pandas(df)

    dd = Dataset_Definition()
    dd.name = 'SampleDataset'
    dd.add_table(td)

    with open('mstrpy/config.2CPU.json', encoding='utf-8', mode='r') as f:
        config = json.load(f)

    conn = Connection(config).connect()
    project = conn.get_project('MicroStrategy Tutorial')

    for ds in project.get_datasets(name='Sample', search_type=SEARCH_TYPE_BEGIN_WITH):
        print(ds.id)
        print(project.get_datasets(id=ds.id))

    print('Creating dataset', flush=True)
    dataset = project.create_dataset(dd)
    print('Updating datasets', flush=True)
    dataset.load_table(td)

if __name__ == '__main__':
    pandas_sample()
