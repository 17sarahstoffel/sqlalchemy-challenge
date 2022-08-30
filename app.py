from flask import Flask

app = Flask(__name__)

@app.route("/")
def Homepage():
    return(
        f"Welcome to the Honolulu, Hawaii Climate App!<br>"
        f"Possible Routes for the App<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"

    )