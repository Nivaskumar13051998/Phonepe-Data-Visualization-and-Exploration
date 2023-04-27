import pandas as pd
import json 
import plotly.express as px
from sqlalchemy import create_engine
from pandas.io import sql
import pymysql


with open(r'C:\Users\Nivas\Downloads\pulse-master\pulse-master\data\map\transaction\hover\country\india\2022\4.json','r') as f:
  datas = json.loads(f.read()),
df_nested_list = pd.json_normalize(datas,record_path =['data','hoverDataList','metric'],meta=['success','code',['data','hoverDataList','name']]) 
df_nested_list


def cap_sentence(s): 
  return ' '.join(w[:1].upper() + w[1:] for w in s.split(' '))




bcd = df_nested_list["data.hoverDataList.name"].str.replace(r'(\w+)', lambda x: x.group().capitalize(),n=2, regex=True)
bcd
df_nested_list['state']=bcd
df_nested_list
df_nested_list.drop(['data.hoverDataList.name'], axis=1,inplace=True)
df_nested_list
engine = create_engine("mysql+pymysql://root:Vasan3390@localhost:8080/phonepe",pool_size=1000, max_overflow=2000)
df_nested_list.to_sql('trans_2022_4', engine, if_exists='append', index=False, chunksize=None, dtype=None, method=None)
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Nivas8080',
                             db='phonepe')




cursor = connection.cursor()
sql='select * from trans_2022_4'
mysql_df=pd.read_sql(sql, engine, index_col=None,chunksize=None)
fig = px.choropleth(
  mysql_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color='count',
    color_continuous_scale='blues'
)

fig.update_geos(fitbounds="locations", visible=False)

fig.show()