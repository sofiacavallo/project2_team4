import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/gunviolence_db_sc"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# states_metadata = Base.classes.gunviolence_db
# states = Base.classes.states

# ABLE TO QUERY TABLE, CODE IS WORKING. JUST ADD CSV AND CONVERT TO JSON
# DATABASE NAME = gunviolence_db_sc
# TABLE IN DATABASE = gunviolence_db
engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
df_gun_violence = pd.read_sql('select * from gunviolence_db', engine)
print(len(df_gun_violence))

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/states")
def list_states():
    """Return a list of states."""

    # Use Pandas to perform the sql query
    engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
    df_gun_violence = pd.read_sql('select * from gunviolence_db', engine)
    
    stmt = list(df_gun_violence['State'].unique())
    # df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (state names)
    return jsonify(stmt)

# METADATA TABLE: Create a summary of gun violence by state. Take relevant information only
# Eg.: exclude "line_number" and "operations" data. 

@app.route("/metadata/<state>")
def gunviolence_metadata(state):
    """Return the gun violence data summary (metadata) for a given state."""
    # sel = [
    #     gunviolence_db.State,
    #     gunviolence_db.year,
    #     gunviolence_db.Incident_ID,
    #     gunviolence_db.Number_Killed,
    #     gunviolence_db.Number_Injured,
    # ]

    # results = db.session.query(*sel).filter(gunviolence_db.State == state).all()
    engine = create_engine("sqlite:///gunviolence_db.sqlite")
    df_gun_violence = pd.read_sql(f"select * from gunviolence_db where State = '{state}' ", engine)
    results = [
        list(df_gun_violence['State']),
        list(df_gun_violence.year),
        list(df_gun_violence['Incident ID'])
    ]
    print('results:', results)

    # [['Wisconsin', 'Wisconsin', 'Wisconsin', 'Wisconsin', 'Wisconsin'], ['2018', '2018', '2018', '2018', '2018'], ['1289543', '1300872', '1290535', '1289545', '1292121']]


# WORK IN JUPYTER NOTEBOOK TO CREATE JSON 
    # Create a dictionary entry for each row of gun violence summary data (metadata)
    # { 'year' : 2018
    #   'incident_counts': "IncidentID".count,
    #   'number_killed': " " 
        ''
    # }
    
    
    gunviolence_metadata = {}
    for result in results:
        print(result)
        # 
        gunviolence_metadata["year"] = result[0]
        gunviolence_metadata["Incident_ID"] = result[1]
        # gunviolence_metadata["Number_Killed"].sum = result[2]
        # gunviolence_metadata["Number_Injured"].sum = result[3]

    # print(gunviolence_metadata)
    return jsonify(gunviolence_metadata)

# Create app route to pull all data points for charts.
@app.route("/states/<state>")
def states(state):
    """Return `incident_ids`, `incident_dates`, `city_or_county`, `number_killed` and `number_injured`."""
    stmt = db.session.query(states).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the state
    state_data = df.loc[df[state], ["incident_id", "incident_date", "city_or_county", "number_killed", "number_injured", State]]

    # Sort by count of city_or_county (highest counts are cities/counties that recorded the most incidents).
    state_data.sort_values(by=city_or_county.count, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "incident_ids": state_data.incident_id.tolist(),
        "incident_dates": state_data.incident_date.tolist(),
        "cities_or_counties": state_data.city_or_county.tolist(),
        "number_killed": state_data.number_killed.tolist(),
        "number_injured": state_data.number_injured.tolist()
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()