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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)


# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
link = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# App Route for opening page
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Hawaiian Climate Analysis API!<br/>   
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/<start><br/>
    /api/v1.0/<start>/<end><br/>
    ''') 

# App Routes for api routes

@app.route("/api/v1.0/precipitation")
def precipitation():
   date_dict = dt.date(2017, 8, 23) - dt.time(days=365)
   precipitation = link.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= date_dict).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = link.query(station.station, station.name).all()
    station_results = {results[i][0]: results[i][1] for i in range(len(results))}
    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
    
def tobs():
    date_dict = dt.date(2017, 8, 23) - dt.time(days=365)
    results = link.query(measurement.tobs).\
      filter(measurement.station == 'USC00519281').\
      filter(measurement.date >= date_dict).all()
    temperature = list(np.ravel(results))
    return jsonify(temperature=temperature)

@app.route("/api/v1.0/<start>")
def start(start):
    temperature_data = link.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    temperature_data = link.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    return jsonify(temperature_data)
    session.close()
if __name__ == "__main__":
    app.run(debug=True)