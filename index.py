from flask import Flask, render_template
from requests.api import get
from get_data import get_bus_stop_data_for_postcode

app = Flask(__name__)

@app.route("/")
def index():
    bus_data = get_bus_stop_data_for_postcode("NW5 1TL")
    bus_stops = bus_data.keys()
    print(bus_stops)
    return render_template('index.html', bus_stops=bus_stops, bus_data=bus_data)