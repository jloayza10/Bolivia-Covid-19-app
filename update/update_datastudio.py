#!/usr/bin/env python3

import pandas as pd
import requests
import json
import datetime as dt

def yesterday():
    """
    Get yesterday in the right format
    """

    return (dt.datetime.now().date() - dt.timedelta(days=1)).strftime('%Y%m%d')

def load_query(query, end_date):
    """
    Load datastudio query, update `end_date`
    """

    with open('update/queries/{}.json'.format(query), 'r') as f:
        json_data = json.load(f)
        json_data['dataRequest'][0]['datasetSpec']['dateRanges'][0]['endDate'] = end_date
        return json_data

def get_data(json_data):
    """
    Query datastudio and get data
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'encoding': 'null',
        'Origin': 'https://lookerstudio.google.com',
        'Alt-Used': 'lookerstudio.google.com',
        'Connection': 'keep-alive',
        'Referer': 'https://lookerstudio.google.com/reporting/92796894-acf3-4ab7-9395-20655de351f7/page/p_zdtrnwnguc',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    params = {
        'appVersion': '20230302_00020115',
    }

    response = requests.post('https://lookerstudio.google.com/batchedDataV2', params=params, headers=headers, json=json_data)
    return response

def extract_values(columns):
    """
    Get values from the datastudio response
    """

    values = []

    for col in columns:
        valuecol = [k for k in col.keys() if 'Column' in k][0]
        values.append(col[valuecol]['values'])

    return values

def build_table(json_data, column_names=['fecha', 'departamento', 'casos']):
    """
    Format values in datastudio response into a nice table
    """

    columns = json_data['dataResponse'][0]['dataSubset'][0]['dataset']['tableDataset']['column']
    values = extract_values(columns)
    df = pd.DataFrame(values).T
    df.columns = column_names
    df['fecha'] = pd.to_datetime(df['fecha'])
    # df['departamento'] = df['departamento'].astype('category')
    df['casos'] = df['casos'].astype(int)
    return df

def make_table_consistent(table):
    """
    Make the table consistent with our older format
    """

    column_order = ['Chuquisaca', 'La Paz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija', 'Santa Cruz', 'Beni', 'Pando']

    table = table.pivot_table(index='fecha', columns='departamento', values='casos')
    table = table[column_order]
    table.index = table.index.set_names('')

    return table

def update_latest(table):
    """
    Get and compare the last update time for a table
    """

    global latest
    table_latest = table.index.max()
    if table_latest > latest:
        latest = table_latest

def print_latest(latest):
    """
    Print the latest update date to format the commit message
    """
    print(latest.strftime('%Y-%m-%d'))

def save(table, query):
    """
    Save cumulative datasets as they are, but only append
    new lines to daily ones.
    """

    if 'diario' in query:
        old_table= pd.read_csv(f'Step_1-Parse/data/{query}.csv', parse_dates=[0], index_col=0)
        newlines = table.loc[old_table.index.max() + dt.timedelta(days=1):]
        table = pd.concat([old_table, newlines])
    table.to_csv(f'Step_1-Parse/data/{query}.csv')

def update_dataset(query):
    """
    Update a dataset
    """

    json_data = load_query(query, end_date)
    response = get_data(json_data)
    table = build_table(json.loads(response.text[6:]))
    table = make_table_consistent(table)
    update_latest(table)
    save(table, query)

latest = pd.Timestamp(year=2020, month=3, day=3)
end_date = yesterday()

for query in ['confirmados_diarios',
              'decesos_diarios',
              'recuperados_diarios',
              'activos_acumulados',
              'confirmados_acumulados',
              'decesos_acumulados',
              'recuperados_acumulados']:
    update_dataset(query)

print_latest(latest)
