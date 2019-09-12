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
# states_metadata = Base.classes.gunviolence_table
# states = Base.classes.states

# ABLE TO QUERY TABLE, CODE IS WORKING. JUST ADD CSV AND CONVERT TO JSON
# DATABASE NAME = gunviolence_db_sc
# TABLE IN DATABASE = gunviolence_table
engine = create_engine("postgresql://postgres:postgres@localhost:5432/gunviolence_db_sc")
df_gun_violence = pd.read_sql('select * from gunviolence_table', engine)
print(len(df_gun_violence))

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/states")
def list_states():
    """Return a list of states."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(gunviolence_table).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (state names)
    return jsonify(list(df.columns)[2:])

# METADATA TABLE: Create a summary of gun violence by state. Take relevant information only
# Eg.: exclude "line_number" and "operations" data. 

@app.route("/metadata/<state>")
def gunviolence_metadata(state):
    """Return the gun violence data summary (metadata) for a given state."""
    sel = [
        gunviolence_table.State,
        gunviolence_table.year,
        gunviolence_table.Incident_ID,
        gunviolence_table.Number_Killed,
        gunviolence_table.Number_Injured,
    ]

    results = db.session.query(*sel).filter(gunviolence_table.State == state).all()
    print('results:', results)

    # Create a dictionary entry for each row of gun violence summary data (metadata)
    gunviolence_metadata = {}
    for result in results:
        print(result)
        gunviolence_metadata["year"] = result[0]
        gunviolence_metadata["Incident_ID"].count = result[1]
        gunviolence_metadata["Number_Killed"].sum = result[2]
        gunviolence_metadata["Number_Injured"].sum = result[3]

    print(gunviolence_metadata)
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