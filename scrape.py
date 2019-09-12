# Declare Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
from flask import request
import html5lib
import pandas as pd
import lxml
import requests
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
import requests as rq
import re
import time 
import random 

# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

a = [1,2,3]
a.extend([4,5])
a

# URL
result = []
list_rows = []
#rows = []
for i in range(0, 17):
    base_url = f'https://www.gunviolencearchive.org/reports/total-number-of-incidents?page={i}&year=2018'
    r = rq.get(base_url)
    time.sleep(random.randint(1,5))
    
    soup = BeautifulSoup(r.text, 'html.parser')
    table_rows = soup.find_all('tr')
    #print('Number of results', len(table_rows))
    for tr in table_rows:
        row_td = tr.find_all('td')
    rows =soup.findAll('tr')
    row = [row.get_text().strip('\n') for row in rows]
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells, "lxml").get_text()
    rows =soup.findAll('tr')
    for row in rows:
        cells = row.find_all('td')
        str_cells = str(cells)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '',str_cells))
        list_rows.append(clean2)

df = pd.DataFrame(list_rows)
df.head(10)

df = pd.DataFrame(list_rows)
df.head(10)

df = df[0].str.split(',', expand=True)
df.head(10)

df[0] = df[0].str.strip('[')
df

headers = rows[0].find_all('th')
headers = [header.get_text().strip('\n') for header in headers]
headers


all_header = []
col_str = str(headers)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)


header = all_header[0].replace('[', '').replace(']', '').split(',')[:8]
header.insert(2, 'year')
# new_header = []
# for item in header:
#     new_header.append(item.strip())
header = [name.replace('"', '').replace("'", "").replace('#', '').strip() for name in header]
header

header_df = pd.DataFrame(header).T
header_df.head()

df.shape, header_df.shape

frames = [header_df, df]

df4 = pd.concat(frames)
df4.head(10)

df5 = df4.rename(columns=df4.iloc[0])
df5.head()

df5.info()
df5.shape

df6 = df5.dropna(axis=0, how='any')

df7 = df6.drop(df6.index[0])
df7.head()

df7['Operations'] = df7['Operations'].str.strip(']').str.strip('\n')
df7.head()

df7 = df7.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

df7.to_csv("gunviolence_db.csv")

# Create engine using the `gunviolence_db.sqlite` database file
engine = create_engine("sqlite:///../project2_team4/gunviolence_db.sqlite")

df7.to_sql("gunviolence_db", con=engine)
