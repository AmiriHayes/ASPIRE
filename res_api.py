# this file is for the demo website: www.aspirefortransport.org

# this file is for the demo website: www.aspirefortransport.org

from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import osmnx as ox
import io
import base64
import matplotlib.pyplot as plt
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
    fig, ax = ox.plot_graph(g, show=False)
    g = g.to_undirected()

    img_bytes = io.BytesIO() 
    plt.savefig(img_bytes, format='png') 
    img_bytes.seek(0) 
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    # processing logic:
    geojson_obj = {"image": img_base64}
    regular_json_obj = {'testkey2': 'testval2'}

    return jsonify({'geojson': geojson_obj, 'json': regular_json_obj})

if __name__ == '__main__':
    app.run(debug=True)
