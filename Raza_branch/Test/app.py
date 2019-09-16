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

# DATABASE NAME = gunviolence_db_sc
# TABLE IN DATABASE = gunviolence_db
engine = create_engine("sqlite:///db/gva1.sqlite")
df_gun_violence = pd.read_sql('select * from gv1', engine)
print(len(df_gun_violence))

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/states")
def list_states():
    """Return a list of states."""

    # Use Pandas to perform the sql query
    engine = create_engine("sqlite:///db/gva1.sqlite")
    df_gun_violence = pd.read_sql('select * from gv1', engine)
    
    stmt = list(df_gun_violence['state'].unique())
    # df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (state names)
    return jsonify(stmt)

# METADATA TABLE: Create a summary of gun violence by state. Take relevant information only
# Eg.: exclude "line_number" and "operations" data. 

@app.route("/metadata/<state>")
def gunviolence_metadata(state):
    """Return the gun violence data summary (metadata) for a given state."""
    # results = db.session.query(*sel).filter(gunviolence_db.State == state).all()
    engine = create_engine("sqlite:///db/gva1.sqlite")
    df_gun_violence = pd.read_sql(f"select * from gv1 where state = '{state}' ", engine)
    results = [
        list(df_gun_violence['state']),
        list(df_gun_violence.date),
        list(df_gun_violence['city_or_county'])
    ]
    gunviolence_metadata = {}
    for result in results:
       # print(result)
        print('1')
        gunviolence_metadata["date"] = result[1]
        gunviolence_metadata["city"] = result[2]
        # gunviolence_metadata["Number_Killed"].sum = result[2]
        # gunviolence_metadata["Number_Injured"].sum = result[3]

    # print(gunviolence_metadata)
    return jsonify(gunviolence_metadata)

# Create app route to pull all data points for charts.
@app.route("/states/<state>")
def states(state):
    """Return `incident_ids`, `date`, `city_or_county`, `killed` and `injured`."""
    stmt = gv1.session.query('state').statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the state
    state_data = df.loc[df[state], ["incident_id", "date", "city_or_county", "killed", "injured", state]]

    # Sort by count of city_or_county (highest counts are cities/counties that recorded the most incidents).
    state_data.sort_values(by=city_or_county.count, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "incident_ids": state_data.incident_id.tolist(),
        "incident_dates": state_data.date.tolist(),
        "cities_or_counties": state_data.city_or_county.tolist(),
        "number_killed": state_data.killed.tolist(),
        "number_injured": state_data.injured.tolist()
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()