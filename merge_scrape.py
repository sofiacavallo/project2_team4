#!/usr/bin/env python
# coding: utf-8
# Import Dependencies
import pandas as pd
from splinter import Browser
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

gunviolence2019_csv = "gunviolence2019_db.csv"
gunviolence2018_csv = "gunviolence2018_db.csv"
gunviolence2017_csv = "gunviolence2017_db.csv"
gunviolence2016_csv = "gunviolence2016_db.csv"
gunviolence2015_csv = "gunviolence2015_db.csv"

gunviolence2019_df = pd.read_csv(gunviolence2019_csv)
gunviolence2018_df = pd.read_csv(gunviolence2018_csv)
gunviolence2017_df = pd.read_csv(gunviolence2017_csv)
gunviolence2016_df = pd.read_csv(gunviolence2016_csv)
gunviolence2015_df = pd.read_csv(gunviolence2015_csv)

gunviolence2019_df.head()

gunviolence2018_df.head()

gunviolence2017_df.head()

gunviolence2016_df.head()

gunviolence2015_df.head(

gunviolence_df = pd.concat([gunviolence2015_df, gunviolence2016_df, gunviolence2017_df, gunviolence2018_df, gunviolence2019_df], join='inner').sort_index()
gunviolence_df


gunviolence_df.to_csv("gunviolence_db.csv")


# Create engine using the `gunviolence_db.sqlite` database file
engine = create_engine("sqlite:///../project2_team4/gunviolence_db.sqlite")


gunviolence_df.to_sql("gunviolence_db", con=engine)

