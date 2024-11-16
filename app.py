import requests
import json
import matplotlib.pyplot as plt
import datetime
import numpy as np
import folium

SANANDREAS_LATITUDE = 35.1167
SANANDREAS_LONGITUDE = -119.6500

def fetch_earthquake_data():
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        'latitude': SANANDREAS_LATITUDE,
        'longitude': SANANDREAS_LONGITUDE,
        'maxradiuskm': 5000,
        "starttime": "2024-11-15",
        "endtime": "2025-09-01",
        "minmagnitude": 1.0,
        "orderby": "time"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch earthquake data.")
        return None

earthquake_data = fetch_earthquake_data()

def parse_earthquake_data(data):
    earthquakes = []

    for feature in data['features']:
        properties = feature['properties']
        magnitude = properties['mag']
        timestamp = datetime.datetime.fromtimestamp(properties['time'] / 1000.0)

        coordinates = feature['geometry']['coordinates']
        longitude = coordinates[0]
        latitude = coordinates[1]

        earthquakes.append({
            'magnitude': magnitude,
            'timestamp': timestamp,
            'longitude': longitude,
            'latitude': latitude

        })

    return earthquakes

earthquakes = parse_earthquake_data(earthquake_data)

locations = []

for quake in earthquakes:
    location = (quake['latitude'],quake['longitude'])
    locations.append(
        location
    )

def plot_earthquake_magnitudes(earthquakes):
    timestamps = [quake['timestamp'] for quake in earthquakes]
    magnitudes = [quake['magnitude'] for quake in earthquakes]
    latitude = [quake['latitude'] for quake in earthquakes]
    longitude = [quake['longitude'] for quake in earthquakes]
   

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(timestamps, magnitudes, marker='o', linestyle='-', color='b')
    plt.title('Earthquake Magnitudes Over Time')
    plt.xlabel('Time')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.xticks(rotation=45)
   
    plt.subplot(1, 2, 2)
    scatter = plt.scatter(longitude, latitude, c=magnitudes, cmap='viridis', marker='.')
    plt.title('Earthquake Location')
    plt.xlabel('Longiitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Magnitude')
    plt.grid(True)

    plt.tight_layout()
    plt.show


plot_earthquake_magnitudes(earthquakes)


mymap = folium.Map(location=[35.0, -118.5], zoom_start=8) 

for lat, lon in locations:
    folium.CircleMarker(
        location=[lat, lon],
        radius=2,      
        color='red',   
        fill=True,      
        fill_color='red',
        fill_opacity=0.8 
    ).add_to(mymap)
mymap
