# this file is for the demo website: www.aspirefortransport.org

from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)

import json
import osmnx as ox
from geopy import geocoders
G = geocoders.GeoNames(username='amiri_hayes_')

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    city_neighborhood = data.get('neighborhood')
    city_name = data.get('city')
    city_state = data.get('state')

    city = city_neighborhood, city_name, city_state
    center = G.geocode(', '.join(city))[-1]
    g = ox.graph_from_point(center_point=center, dist=1000, network_type="walk")
    g = g.to_undirected()

    nodes, edges = ox.graph_to_gdfs(g) 
    edges = edges[["geometry"]]
    geojson_img = json.loads(edges.to_json())

    # processing logic:
    geojson_obj = geojson_img
    regular_json_obj = {'testkey2': 'testval2'}

    return jsonify({'geojson': geojson_obj, 'json': regular_json_obj})

if __name__ == '__main__':
    app.run(debug=True)
