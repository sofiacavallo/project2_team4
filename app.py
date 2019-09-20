import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_debug import Debug
from werkzeug.debug import DebuggedApplication

def create_app():

    app = Flask(__name__)
    app.debug=True


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
        raise Exception()

    @app.route("/State")
    def list_states():
        """Return a list of states."""

        # Use Pandas to perform the sql query
        engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
        df_gunviolence_states = pd.read_sql('select State from gunviolence_db', engine)
        
        stmt = list(df_gunviolence_states.sort_values(by=['State'])['State'].unique())

        # Return a list of the column names (state names)
        return jsonify(stmt)

    # METADATA TABLE: Create a summary of gun violence by state. 
    @app.route("/metadata/<State>")
    def gunviolence_metadata(State):
        """Return the gun violence data summary (metadata) for a given state."""

        engine = create_engine("sqlite:///db/gunviolence_db.sqlite")
        df_gunviolence_metadata = pd.read_sql(f"select * from gunviolence_db where State = '{State}' ", engine)
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
    @app.route("/states/<State>")
    def states(State):
        """Return `incident_ids`, `incident_dates`, `city_or_county`, `number_killed` and `number_injured`."""

        # Filter the data based on the state
        df_gunviolence_bystate = pd.read_sql(f"select * from gunviolence_db where State = '{State}' ", engine)

        # Format the data to send as json
        data = {
            "incident_ids": df_gunviolence_bystate["Incident ID"].tolist(),
            "incident_dates": df_gunviolence_bystate["Incident Date"].tolist(),
            "cities_or_counties": df_gunviolence_bystate["City Or County"].tolist(),
            "number_killed": df_gunviolence_bystate["Killed"].tolist(),
            "number_injured": df_gunviolence_bystate["Injured"].tolist()
        }
        return jsonify(data)
        
    #states('Wisconsin')

    if __name__ == "__main__":
     app.run()
    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
        
        return app