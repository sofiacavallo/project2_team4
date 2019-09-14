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

engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
df_gunviolence = pd.read_sql('select * from gunviolence_db', engine)
print(len(df_gunviolence))

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/states")
def list_states():
    """Return a list of states."""

    # Use Pandas to perform the sql query
    engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
    df_gunviolence = pd.read_sql('select State from gunviolence_db', engine)
    
    stmt = list(df_gunviolence.sort_values(by=['State'])['State'].unique())

    # Return a list of the column names (state names)
    return jsonify(stmt)
    return stmt

# METADATA TABLE: Create a summary of gun violence by state. 
@app.route("/metadata/<state>")
def gunviolence_metadata(state):
    """Return the gun violence data summary (metadata) for a given state."""

    engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
    df_gunviolence_metadata = pd.read_sql(f"select * from gunviolence_db where State = '{state}' ", engine)
    df_gunviolence_metadata["Killed"] = df_gunviolence_metadata["Killed"].astype(int)
    df_gunviolence_metadata["Injured"] = df_gunviolence_metadata["Injured"].astype(int)
            
    # Create a dictionary entry for each row of gun violence summary data (metadata)
    gunviolence_metadata = {
        "Incident_ID": df_gunviolence_metadata['Incident ID'].value_counts().sum(), 
        "Number_Killed": df_gunviolence_metadata[df_gunviolence_metadata["Killed"] > 0]["Killed"].value_counts().sum(),
        "Number_Injured": df_gunviolence_metadata[df_gunviolence_metadata["Injured"] > 0]["Injured"].value_counts().sum()
    }
    
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