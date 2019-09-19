# Dependencies
# Declare Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup
from flask import request
import html5lib
import pandas as pd
import lxml
import requests

# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# URL
url = 'https://www.gunviolencearchive.org/reports/total-number-of-incidents?year=2018'
browser.visit(url)

# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())

rows =soup.findAll('tr')
print(rows[:10])

headers = rows[0].find_all('th')
headers = [header.get_text().strip('\n') for header in headers]
headers

row = rows[0].find_all('tr')
row = [row.get_text().strip('\n') for row in rows]
row

for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)

str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)


import re

list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)

df = pd.DataFrame(list_rows)
df.head(10)


df1 = df[0].str.split(',', expand=True)
df1.head(10)


df1[0] = df1[0].str.strip('[')
df1.head(10)

col_labels = soup.find_all('th')

all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)

header = all_header[0].replace('[', '').replace(']', '').split(',')[:8]
header.insert(2, 'year')
# new_header = []
# for item in header:
#     new_header.append(item.strip())
header = [name.strip() for name in header]
header

df2 = pd.DataFrame(header).T
df2.head()

df3 = df2[0].str.split(',', expand=True)
df3.head()

df1.shape, df2.shape

frames = [df2, df1]

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

