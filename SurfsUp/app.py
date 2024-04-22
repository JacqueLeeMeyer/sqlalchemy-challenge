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
# When using:engine = create_engine("sqlite:///hawaii.sqlite") or any other variation, the classes return an AttributeError
# Therfore the path is not a reletive path... this is the only way it would run for me!
engine = create_engine("sqlite:///Module10\Module10_Challenge\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Route: home
@app.route("/")
def home():
    # Show list of routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
       
    )

# Route: precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    # Most recent date
    recent_date = dt.date(2017, 8, 23)
    
    # Date one year before the most recent date in data set
    early_date = recent_date - dt.timedelta(days=365)

    # Query to retrieve the data and precipitation scores
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= early_date).all()

    # Create Dictionary from results and jsonify
    precipitation = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

# Route: stations
@app.route("/api/v1.0/stations")
def stations():
    # Query to find station ids
    station_data = session.query(Station.station).all()

    # Create List and jsonify
    station_list = list(np.ravel(station_data))
    return jsonify(station_list)

# Route: temps
@app.route("/api/v1.0/tobs")
def temps():
    # Most recent date
    recent_date = dt.date(2017, 8, 23)
    
    # Date one year before the most recent date in data set
    early_date = recent_date - dt.timedelta(days=365)

    temps = session.query(Measurement.tobs).\
        filter(Measurement.date >= early_date).\
        filter(Measurement.station == 'USC00519281').all()

    # Create List and jsonify
    temps_list = list(np.ravel(temps))
    return jsonify(temps_list)

# Route: start
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    temp_results = session.query(func.min(Measurement.tobs), 
                                 func.max(Measurement.tobs), 
                                 func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
   # Create Dictionary from results and jsonify
    temp_list = []
    for result in temp_results:
        temp_dict = {}
        temp_dict["Min Temp"] = result[0]
        temp_dict["Max Temp"] = result[1]
        temp_dict["Avg Temp"] = result[2]
        temp_list.append(temp_dict)

    return jsonify(temp_list)

# Route: start/end
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    temp_results2 = session.query(func.min(Measurement.tobs), 
                                 func.max(Measurement.tobs), 
                                 func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

   # Create Dictionary from results and jsonify
    temp_list2 = []
    for result in temp_results2:
        temp_dict = {}
        temp_dict["Min Temp"] = result[0]
        temp_dict["Max Temp"] = result[1]
        temp_dict["Avg Temp"] = result[2]
        temp_list2.append(temp_dict)

    return jsonify(temp_list2)

if __name__ == '__main__':
    app.run(debug=True)

# Close Session
session.close()
