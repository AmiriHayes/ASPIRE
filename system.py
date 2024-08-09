# ASPIRE: Transportation Scoring Metric
# Created By: Amiri Hayes
# Last Updated: 12/13/2023
# Contact: akh5 @ njit.edu
# Read The Paper: tinyurl.com/ASPIRE4Transportation

import os
import json
import requests
import numpy as np
from glob import glob
from tqdm import tqdm

import random
import osmnx as ox
import numpy as np
import pandas as pd
import networkx as nx
from geopy import geocoders
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
G = geocoders.GeoNames(username='amiri_hayes_')

class Data_Factory:
  def __init__(self, city):
    self.city_neighborhood, self.city_name, self.city_state = city
    self.coordinates = G.geocode(', '.join(city))[-1]
    self.timezone = G.reverse_timezone(self.coordinates)._raw["timezoneId"]

  def get_infrastructure(self):
    g = ox.graph_from_point(center_point=self.coordinates, dist=1000, network_type="walk")
    # fig, ax = ox.plot_graph(g)
    g = nx.Graph(g)

    centrality_values = nx.degree_centrality(g)
    centrality = sum(centrality_values.values()) / len(centrality_values)
    degree = sum(dict(g.degree()).values()) / g.number_of_nodes()
    density = nx.density(g)
    efficiency = nx.global_efficiency(g)
    closeness = max(nx.closeness_centrality(g).values())

    return [centrality, degree, density , efficiency, closeness]

  def get_environment(self, timezone):
    tz = timezone.replace("/", "%2F")
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&daily=sunset&timezone={tz}&past_days=14&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,rain&temperature_unit=fahrenheit"
    response = requests.get(url = URL).json()

    if response:
      temp_avg = round(sum(response["hourly"]["temperature_2m"]) / len(response["hourly"]["temperature_2m"]), 2)
      humidity_avg = round(sum(response["hourly"]["relativehumidity_2m"]) / len(response["hourly"]["relativehumidity_2m"]), 2)
      windspeed_avg = round(sum(response["hourly"]["windspeed_10m"]) / len(response["hourly"]["windspeed_10m"]), 2)
      rain_avg = round(sum(response["hourly"]["rain"]) / len(response["hourly"]["rain"]), 2)

      sunset_seconds, ftr = [], [60, 1]
      sunset_res = [val.split("T")[1] for val in response["daily"]["sunset"]]
      for val in sunset_res:
        sunset_seconds.append(sum([a*b for a,b in zip(ftr, map(int,val.split(':')))]))
      sunset_avg = round(sum(sunset_seconds) / len(sunset_seconds), 2)

    return [temp_avg, humidity_avg, windspeed_avg, rain_avg, sunset_avg]

  def get_safety(self):
    api_key = "NFiL07Qb2reRBmseXIecRMpnfEIA7uO6Ps1n7QXS"
    crimes = ["aggravated-assault", "violent-crime", "robbery", "arson",
              "homicide", "burglary", "motor-vehicle-theft", "larceny", "property-crime"]

    crime_stats = []
    for crime in crimes:
      URL = f"https://api.usa.gov/crime/fbi/cde/estimate/state/{self.state}/{crime}?from=2020&to=2023&API_KEY={api_key}"
      response = requests.get(url = URL).json()

      if response and response["results"] != "null":
        crime_value = -1
        response = response["results"]

        try: crime_stat = next(iter(response.values()))
        except: continue

        crime_stat = next(iter(crime_stat.values()))
        if isinstance(crime_stat, (int, float, complex)) and not isinstance(crime_stat, bool):
            crime_value = crime_stat
      crime_stats.append(crime_value)
      
    return crime_stats

  def get_population(self):
      pass

  def get_aesthetic(self):
      pass

  def get_economic(self):
      pass

# ————— #

class Walk_Score():
  def __init__(self, factory_data):
    pass

  def get_proximity(self):
    walkscore = -1
    apikey = "9ae2d037ce429437b95c435494d6e126"
    [lat, lon] = G.geocode(', '.join(city))[-1]

    URL = f"https://api.walkscore.com/score?format=json&address=0&lat={lat}&lon={lon}&transit=1&bike=1&wsapikey={apikey}"
    response = requests.get(url = URL).json()
    if response["walkscore"]: walkscore = response["walkscore"]
    
    return walkscore

  def get_connectivity(self):
    pass

  def develop_model(self):
    pass
  
  def return_score(self, city):
    pass
    
# ————— #

class Bike_Score():
  def __init__(self, factory_data):
    pass
  
  def get_lanes(self):
    pass

  def get_accidents(self):
    # implementation for bike accidents data retrieval
    pass

  def get_bike_costs(self):
    # implementation for bike costs data retrieval
    pass

  def develop_model(self):
    pass
  
  def return_score(self):
    pass

# ————— #

class Drive_Score():
  def __init__(self, factory_data):
    pass

  def get_car_costs(self):
      # implementation for car costs data retrieval
      pass

  def get_congestion(self):
      # implementation for congestion data retrieval
      pass

  def get_parking(self):
      # implementation for parking data retrieval
      pass
  
  def develop_model(self):
    pass
  
  def return_score(self):
    pass

# ————— #

class Public_Transport_Score():
  def __init__(self, factory_data):
    pass

  def get_ridership(self):
      # implementation for public transport ridership data retrieval
      pass

  def get_frequency(self):
      # implementation for public transport frequency data retrieval
      pass

  def get_coverage(self):
      # implementation for public transport coverage data retrieval
      pass
  
  def develop_model(self):
    pass
  
  def return_score(self):
    pass

# ————— #

def data_to_json(city):
  factory = Data_Factory(city)
  cached_file = f'assets/{city(0).replace(" ", "_")}+{city(1).replace(" ", "_")}.json'

  data = {
    "infrastructure": factory.get_infrastructure(),
    "environment": factory.get_environment(),
    "safety": factory.get_safety(),
    "population": factory.get_population(),
    "aesthetic": factory.get_aesthetic(),
    "economic": factory.get_economic(),
  }

  with open(cached_file, 'w') as f: f.write(json.dumps(data, indent=4, sort_keys=True))
  return data

cities = pd.read_csv('../cities.csv', delimiter='\t')
print("Training Data Size is", len(cities))

dataset = []
for city in tqdm(cities):
  city_data = data_to_json(city)
  dataset.append(city_data)

walk = Walk_Score(dataset)
walk.develop_model()

bike = Bike_Score(dataset)
bike.develop_model()

drive = Drive_Score(dataset)
drive.develop_model()

public = Public_Transport_Score(dataset)
public.develop_model()

test_city = cities[0]
test_city_scores = [
                    walk.return_score(test_city), 
                    bike.return_score(test_city), 
                    drive.return_score(test_city), 
                    public.return_score(test_city), 
                   ]