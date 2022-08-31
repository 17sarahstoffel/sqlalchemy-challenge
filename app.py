#bring in dependencies
import json
from tracemalloc import start
import numpy as np
import datetime as dt

#Python SQL toolkit and ORM
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#######################################
#Set up DataBases
#######################################

#create engine and reflect the tables
engine = create_engine("sqlite:///Data/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)

#collect the keys and create reference table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station


#######################################
#Create App
#######################################
app = Flask(__name__)

#create homepage
@app.route("/")
def Homepage():
    return(
        f"Welcome to the Honolulu, Hawaii Climate App!<br>"
        f"Possible Routes for the App<br>"
        f"Precipitation: /api/v1.0/precipitation<br>"
        f"Stations: /api/v1.0/stations<br>"
        f"Temperature: /api/v1.0/tobs<br>"
        f"Temperature from a given start date: /api/v1.0/yyyy-mm-dd<br>"
        f"Temperature from a given start-end range: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

#create precipitation page
@app.route("/api/v1.0/precipitation")
def Precipitation():
    #link python to database
    session = Session(engine)

    precipitation = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    session.close()

    #turn into dictionary
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp

        prcp_data.append(prcp_dict)

    #pring json
    return jsonify(prcp_data)

#create station page
@app.route("/api/v1.0/stations")
def Stations():
    #link to python to database
    session = Session(engine)

    stations = session.query(Station.station).all()
    session.close()

    #turn the data into a list
    station_list = list(np.ravel(stations))
    return jsonify(station_list)


#create temp page
@app.route("/api/v1.0/tobs")
def Temps():
    #link python to database
    session =Session(engine)
    
    temps= session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session.close()

    #put data into a dictionary
    temp_list =[]
    for date, tobs in temps:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs

        temp_list.append(temp_dict)

    return jsonify(temp_list)

#create start date page
@app.route('/api/v1.0/<start_date>')
def Start_date(start_date):
    #link python to database
    session=Session(engine)

    start_day = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    #create a dictionary for the data
    start_date_list =[]
    for max, min, avg in start_day:
        start_dict ={}
        start_dict['max'] = max
        start_dict['min']= min
        start_dict['avg'] = avg

        start_date_list.append(start_dict)
    return jsonify(start_date_list)

@app.route('/api/v1.0/<start_date>/<end_date>')
def start_date_end_date(start_date, end_date):
    #link python to database
    session = Session(engine)
    
    start_end = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    #create a dictionary for the data
    start_end_data = []
    for max,min,avg in start_end:
        start_end_dict = {}
        start_end_dict['max']= max
        start_end_dict['min']= min
        start_end_dict['avg']= avg

        start_end_data.append(start_end_dict)

    return jsonify(start_end_data)


if __name__ =="__main__":
    app.run(debug=True)