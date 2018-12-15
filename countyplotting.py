import geopandas
import plotly
import plotly.plotly as py
import plotly.figure_factory as ff
plotly.tools.set_credentials_file(username='ogghead', api_key='EsWrP3QyXnrebM4IBNBZ')

import pandas as pd

df =  pd.read_csv('election_dataframe.csv')

fips = df['FIPS Code'].values
df.fillna(df.mean(), inplace=True)
#Change data to any category name you want to see plotted
data = df['Republicans 2016'].values
bnpnts = [i for i in range(int(data.min()), int(data.max() + (data.max()-data.min())/6), int((data.max()-data.min())/6))]
colors = [
    'rgb(0,0,102)',
    'rgb(0,0,153)',
    'rgb(0,0,204)',
    'rgb(51,51,255)',
    'rgb(153,153,255)',
    'rgb(255,153,153)',
    'rgb(255,51,51)',
    'rgb(204,0,0)',
    'rgb(102,0,0)'
]
fig = ff.create_choropleth(fips=fips, values=data, binning_endpoints = bnpnts, colorscale = colors)
py.iplot(fig, filename='choropleth_full_usa')




