import pandas as pd
import numpy as np
import json
from functools import reduce


# Strings needed to read github data
url_names = ["confirmados_diarios.csv","decesos_diarios.csv",
             "recuperados_diarios.csv","confirmados_acumulados.csv",
             "activos_acumulados.csv","decesos_acumulados.csv",
             "recuperados_acumulados.csv"]
url_base = "https://raw.githubusercontent.com/sociedatos/covid19-bo-casos_por_departamento/master/"
df_names = ["df_daily_pos","df_daily_deaths","df_daily_recup","df_acc_pos",
            "df_acc_act","df_acc_deaths","df_acc_recup"]
ciudades = ['Chuquisaca','La Paz','Cochabamba','Oruro','Potosi','Tarija',
            'Santa Cruz','Beni','Pando', 'Bolivia']
df_dict = {}
tipos = ['Positivos', 'Muertes', 'Recuperados','Total Positivos','Total Activos',
                        'Total Muertes','Total Recuperados']
data_poblacion = {'Ciudad':['Chuquisaca','La Paz','Cochabamba','Oruro','Potosi',
                            'Tarija','Santa Cruz','Beni','Pando', 'Bolivia'],
                  'Poblacion':[654000, 3023800, 2086900, 548500, 907700, 591800, 3363400, 507100,
                     158700, 11842000]}
df_poblacion = pd.DataFrame(data_poblacion) # country and departamento population

# Func to read the data
def read_github_csv(url,name):
    df_dict[name] = pd.read_csv(url_base + url,
                                names=('Fecha','Chuquisaca','La Paz','Cochabamba',
                               'Oruro','Potosi','Tarija','Santa Cruz','Beni',
                               'Pando'),
                                skiprows=1,
                                parse_dates=[0])
# Change city columns to rows
def df_melt(df,valor):
    return df.melt(id_vars=['Fecha'],
                   value_vars=['Chuquisaca','La Paz','Cochabamba','Oruro',
                               'Potosi','Tarija','Santa Cruz','Beni','Pando',
                               'Bolivia'],
                   var_name='Ciudad', value_name=valor)
# Number of cases, deaths and recovered per 100,000 uses a 14-day average
def col_per_100k(df,col_name):
    df[col_name+' por 100k hab.']= (df[col_name+'_avg14']*100000) / df['Poblacion']

# read and create a dict of dataframes for each url
for url, name in zip(url_names,df_names):
    read_github_csv(url,name)
# create new col for the whole country for each df
for df in df_dict.values():
    df["Bolivia"]=df.iloc[:, -9:].sum(axis=1)

dataframes_list = []
for df, tipo in zip(df_dict.values(), tipos):
    dataframes_list.append(df_melt(df,tipo))

#JSON manipaulation for geo data
deptos_map = {}
Bolivia_deptos = json.load(open("../../../Step_0-Raw/data/departamentos_Bolivia.geojson",'r'))
for feature in Bolivia_deptos['features']:
    deptos_map[feature["properties"]['NOM_DEP'].title()] = feature['id']

#create whole dataframe with each city dataframe
df_covid_Bolivia = reduce(lambda left,right: pd.merge(left,right,on=['Fecha','Ciudad'],
                                            how='outer'), dataframes_list)

# order the dataframe by date and departamento
condition = (df_covid_Bolivia.Ciudad=='Bolivia')
excluded = df_covid_Bolivia[condition]
included = df_covid_Bolivia[~condition]
sorted1 = included.sort_values(['Fecha','Ciudad'], ascending=True)
df_covid_Bolivia = pd.concat([sorted1,excluded])
# provide total population for each city
df_covid_Bolivia = pd.merge(df_covid_Bolivia,
                            df_poblacion,
                            how='left',
                            on='Ciudad')
df_covid_Bolivia["id"] = df_covid_Bolivia.loc[df_covid_Bolivia["Ciudad"]!="Bolivia"]["Ciudad"].apply(lambda x: deptos_map[x])
df_covid_Bolivia['Fecha_str'] = [d.strftime('%d %B, %Y') for d in pd.to_datetime(df_covid_Bolivia['Fecha'])]
df_covid_Bolivia['Fecha_str2'] = [d.strftime('%d-%m-%Y') for d in pd.to_datetime(df_covid_Bolivia['Fecha'])]

# sort by date with Bolivia included
df_covid_Bolivia = df_covid_Bolivia.assign(simplified_a = np.where(df_covid_Bolivia.Ciudad =='Bolivia', 0, df_covid_Bolivia.Ciudad))\
  .sort_values(["Fecha","simplified_a"], ascending=True).drop("simplified_a", axis=1)


# Rolling averages dataframes
df_promedios_7 = df_covid_Bolivia[['Ciudad', 'Positivos', 'Muertes', 'Recuperados']]\
    .groupby("Ciudad").rolling(window = 7).mean().reset_index().set_index('level_1')
df_promedios_14 = df_covid_Bolivia[['Ciudad', 'Positivos', 'Muertes', 'Recuperados']]\
    .groupby("Ciudad").rolling(window = 14).mean().reset_index().set_index('level_1')


# Join rolling averages to principal df
df_all = df_covid_Bolivia.join(df_promedios_7,rsuffix='_avg7')
df_all = df_all.join(df_promedios_14,rsuffix='_avg14')
df_all.drop(['Ciudad_avg7','Ciudad_avg14'],axis=1,inplace=True)

for tipo in ['Positivos', 'Muertes', 'Recuperados']:
    col_per_100k(df_all,tipo)

df_monthly_mean = df_all.groupby(["Ciudad",pd.PeriodIndex(df_all.Fecha,freq='M')],axis=0)[['Positivos', 'Muertes', 'Recuperados']].mean().reset_index()
df_weekly_mean = df_all.groupby(["Ciudad",pd.PeriodIndex(df_all.Fecha, freq='W')], axis=0)[['Positivos', 'Muertes', 'Recuperados']].mean().reset_index()
df_weekly_mean['Last_day_week'] = df_weekly_mean['Fecha'].dt.to_timestamp(how='e').dt.strftime('%Y-%m-%d')
df_weekly_mean['wk-AA'] = df_weekly_mean['Fecha'].dt.to_timestamp(how='e').dt.strftime('%V-%Y')
df_monthly_mean['Fecha_str'] = df_monthly_mean['Fecha'].dt.to_timestamp(how='s').dt.strftime('%m-%Y')
included_monthly = df_monthly_mean[~(df_monthly_mean.Ciudad=='Bolivia')]
included_weekly = df_weekly_mean[~(df_weekly_mean.Ciudad=='Bolivia')]
df_monthly_mean["id"] = included_monthly["Ciudad"].apply(lambda x: deptos_map[x])
df_weekly_mean["id"] = included_weekly["Ciudad"].apply(lambda x: deptos_map[x])

df_all.to_pickle('../data/df_covid_Bolivia.pickle',protocol=3)
df_monthly_mean.to_pickle('../data/df_monthly_mean.pickle',protocol=3)
df_weekly_mean.to_pickle('../data/df_weekly_mean.pickle',protocol=3)
