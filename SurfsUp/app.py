# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station=Base.classes.station
Measurement=Base.classes.measurement

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Route:home
@app.route("/")
def home():
    #Show list of routes
    "List all available route"
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


#Route:precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    #Open Session
    session = Session(engine)

    #Most recent date.
    recent_date=dt.date(2017, 8, 23)
    
    # Date one year before the most recent date in data set.
    early_date=recent_date - dt.timedelta(days=365)

    # Query to retrieve the data and precipitation scores
    precip_data=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= early_date).all()
    
    #Close Session
    session.close()

    #Create Dictionary from results and jsonify.
    precipitation = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)
    return jsonify(precipitation)

#Route:stations
@app.route("/api/v1.0/stations")
def stations():
    #Open Session
    session = Session(engine)

    #Query to find station ids
    station=session.query(Station.station).all()
    
    #Close Session
    session.close()

    #Create List and jsonify
    station_list=list(np.ravel(station))
    return jsonify(station_list)

#Route:temps
@app.route("/api/v1.0/tobs")
def temps():
    # Open Session
    session = Session(engine)

    # Most recent date.
    recent_date=dt.date(2017, 8, 23)
    
    # Date one year before the most recent date in data set.
    early_date=recent_date - dt.timedelta(days=365)
    temps=session.query(Measurement.tobs).\
    filter(Measurement.date >= early_date).\
    filter(Measurement.station=='USC00519281').all()

    # Close Session
    session.close()

    #Create List and jsonify
    temps_list=list(np.ravel(temps))
    return jsonify(temps_list)

# #Route:start
# @app.route()
# def start():
#     # Open Session
#     session = Session(engine)


#     # Close Session
#     session.close()


# #Route:start/end
# @app.route()
# def start_end():
#     # Open Session
#     session = Session(engine)


#     # Close Session
#     session.close()

if __name__ == '__main__':
    app.run(debug=True)