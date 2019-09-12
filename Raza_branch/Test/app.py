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


# #################################################
# # Database Setup
# #################################################
# app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/gva1.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Samples_Metadata = Base.classes.gva1
# Samples = Base.classes.gva1


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


# @app.route("/samples")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Samples).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.date,
#         Samples_Metadata.state,
#         Samples_Metadata.city_or_county,
#         Samples_Metadata.killed,
#         Samples_Metadata.injured,
#         Samples_Metadata.district,
#         Samples_Metadata.latitude,
#         Samples_Metadata.longitude
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["Date"] = result[0]
#         sample_metadata["State"] = result[1]
#         sample_metadata["City or County"] = result[2]
#         sample_metadata["# Killed"] = result[3]
#         sample_metadata["# Injured"] = result[4]
#         sample_metadata["District"] = result[5]
#         sample_metadata["Latitude"] = result[6]
#         sample_metadata["Longitude"] = result[7]

#     print(sample_metadata)
#     return jsonify(sample_metadata)


if __name__ == "__main__":
    app.run()
