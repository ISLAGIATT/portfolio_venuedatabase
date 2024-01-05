# TODO: add edit functionality
# TODO: clean up unused template bits
# TODO: use nicer css

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from forms import VenueForm
from datetime import datetime
import csv
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "4SlaZdAmjtYDyMlz8XuYRaABzBVDIgwY"

Bootstrap5(app)

csv_file_path = os.path.join(os.path.dirname(__file__), 'venue-data.csv')

TOMTOM_API_KEY = "4SlaZdAmjtYDyMlz8XuYRaABzBVDIgwY"

def get_venue_data(venue_name):
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['venue_name'] == venue_name:
                    return row
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return None

def get_coordinates(address):
    url = f"https://api.tomtom.com/search/2/geocode/{address}.json?key={TOMTOM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['position']['lat']
            longitude = data['results'][0]['position']['lon']
            print(latitude, longitude)
            return latitude, longitude
    return None, None

def get_map_image_url(address):
    latitude, longitude = get_coordinates(address)
    if latitude and longitude:
        bbox = f"{longitude-0.01},{latitude-0.01},{longitude+0.01},{latitude+0.01}"
        map_image_url = (f"https://api.tomtom.com/map/1/staticimage?layer=basic&style=main&format=png&zoom=15&center={longitude},{latitude}&width=512&height=512&view=Unified&key={TOMTOM_API_KEY}")
        #map_image_url = (f"https://api.tomtom.com/map/1/tile/basic/main/0/{longitude},{latitude}.png?tileSize=256&view=Unified&language=NGT&key={TOMTOM_API_KEY}")
        print(map_image_url)
        return map_image_url
    return None

@app.route("/")
def home():
    data = []
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")

    return render_template("index.html", data=data)


@app.route("/id:<venue_name>")
def view_venue(venue_name):
    venue_data = get_venue_data(venue_name)

    if venue_data:
        address = venue_data['venue_address']
        map_image_url = get_map_image_url(address)

        if map_image_url:
            venue_data['map_image_url'] = map_image_url
            return render_template("view_venue.html", venue_data=venue_data)
        else:
            # Handle case where map image URL is not available
            return "Map image not available"
    else:
        # Handle case where venue data is not found
        return "Venue not found"

@app.route("/add", methods=['GET', 'POST'])
def add_venue():
    form = VenueForm()
    data = request.form
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%m/%d/%y")

    if form.validate_on_submit():
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            venue_writer = csv.writer(csv_file)
            venue_list = [data['venue_name'], data['venue_address'], data['venue_img_link'], data['venue_url'],
                          data['venue_indoor'],data['venue_owner'], data['venue_refrigeration'], data['can_cook'],
                          data['back_entrance'],data['service_area_size'], formatted_timestamp]

            venue_writer.writerow(venue_list)
            print('venue added')
            return redirect(url_for('home'))

    return render_template("add_venue.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)