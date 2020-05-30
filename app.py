# Import Flask dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependency
from flask import Flask, jsonify

# Set up the database
# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect the database into our classes
Base = automap_base()
# Reflect the table
Base.prepare(engine, reflect=True)
# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session link from Python to our database
session = Session(engine)

# Set up Flask
# Create a New Flask App Instance
app = Flask(__name__)
# Create Flask Routes
@app.route('/')
# Add the routing information for each of the other routes, create a welcome() function
def welcome():
	return(
	'''
	Welcome to the Climate Analysis API!
	Available Routes:
	/api/v1.0/precipitation
	/api/v1.0/stations
	/api/v1.0/tobs
	/api/v1.0/temp/start/end
	''')

# Route for precipitation analysis
@app.route("/api/v1.0/precipitation")
# Define precipitaion function
def precipitation():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	precipitation = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date >= prev_year).all()
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)

# Define stations route
@app.route("/api/v1.0/stations")
# Create stations function
def stations():
	results = session.query(Station.station).all()
	stations = list(np.ravel(results))
	return jsonify(stations)

# Define route for temperature
@app.route("/api/v1.0/tobs")
# Create temperature function
def temp_monthly():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	results = session.query(Measurement.tobs).\
	filter(Measurement.station == 'USC00519281').\
	filter(Measurement.date >= prev_year).all()
	temps = list(np.ravel(results))
	return jsonify(temps)

# Route for min, max and avg temps, statistics function
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create stats() funtion
def stats(start=None, end=None):
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

	if not end: 
		results = session.query(*sel).\
		filter(Measurement.date >= start).all()
		temps = list(np.ravel(results))

		return jsonify(temps)

	results = session.query(*sel).\
	filter(Measurement.date >= start).\
	filter(Measurement.date <= end).all()
	temps = list(np.ravel(results))
	return jsonify(temps)


if __name__ == "__main__":
	app.run(debug=True)