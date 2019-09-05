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

################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gunviolence_db.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
states_metadata = Base.classes.state_metadata
states = Base.classes.states

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/states")
def states():
    """Return a list of states."""
    # Use Pandas to perform the sql query
    stmt = db.session.query(states).statement
    df = pd.read_sql_query(stmt, db.session.bind)

# Return a list of the column names (state names)
    return jsonify(list(df.columns)[2:])

# METADATA TABLE: Create a summary of gun violence by state. Take relvant information only
# Eg.: exclude "line_number" and "operations" data. 

@app.route("/metadata/<state>")
def state_metadata(state):
    """Return the gun violence data summary (metadata) for a given state."""
    sel = [
        states_metadata.State,
        states_metadata.year,
        states_metadata.Incident_ID,
        states_metadata.Number_Killed,
        states_metadata.Number_Injured,
    ]
    
    results = db.session.query(*sel).filter(states_metadata.state == state).all()

    # Create a dictionary entry for each row of gun violence summary data (metadata)
    state_metadata = {}
    for result in results:
        state_metadata["year"] = result[0]
        state_metadata["Incident_ID"].count = result[1]
        state_metadata["Number_Killed"].sum = result[2]
        state_metadata["Number_Injured"].sum = result[3]
        print(state_metadata)
    return jsonify(state_metadata)

# Create app route to pull all data points for charts.
@app.route("/states/<state>")
def states(state):
    """Return `incident_ids`, `incident_dates`, `city_or_county`, `number_killed` and `number_injured`."""
    stmt = db.session.query(states).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    # Filter the data based on the state
    state_data = df.loc[df[state], ["incident_id", "incident_date", "city_or_county", "number_killed", "number_injured", state]]
    
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