'''
This code generate a choromap of world capitals with current temperatures.
'''
from bs4 import BeautifulSoup
import requests
import csv
import plotly
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
init_notebook_mode(connected=True)
import pandas as pd

source = requests.get('https://www.timeanddate.com/weather/?low=c').text

soup = BeautifulSoup(source, 'lxml')

city = []
temp = []
country = []
main_table = soup.find('table', class_='zebra fw tb-theme')

for i in main_table.find_all('a',href=True):
    country.append(i['href'])
    city.append(i.text)

for i in main_table.find_all('td',class_='rbi'):
    temp.append(i.text)

temp = [i.replace('\xa0°C','') for i in temp]
country = [i.split('/')[2].capitalize() for i in country]
all_info = list(zip(country,city,temp))
print(all_info)

location = input("Insert path (with '\\' at the end) to location in which you would like to save .csv file with data: ")

with open(location+'temp_info.csv','w',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Country','Capital','Temp'])
    for info in all_info:
        writer.writerow([info[0],info[1],info[2]])

temp_file = location+'temp_info.csv'
df = pd.read_csv(temp_file)

data = dict(type='choropleth',
           locations = df['Country'],
            colorscale = 'Portland',
           locationmode = 'country names',
           z = df['Temp'],
           text = df['Capital'],
           colorbar = {'title':'Temperature in °C'})
layout = dict(title = 'Current temperature for world capitals',
             geo = dict(showframe=False,
                     projection = {'type':'kavrayskiy7'}))

choromap = go.Figure(data = [data],layout = layout)
#iplot(choromap,validate=False) --> to plot in jupyter notebook
plotly.offline.plot(choromap)
