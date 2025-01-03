# this file is for the demo website: www.aspirefortransport.org

from flask import Flask, request, jsonify
from flask_cors import CORS
import osmnx

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    param1 = data.get('param1')
    param2 = data.get('param2')
    # Add your processing logic here
    geojson_obj = {'testkey1': 'testval1'}  # your GeoJSON object
    regular_json_obj = {'testkey2': 'testval2'}  # your regular JSON object
    return jsonify({'geojson': geojson_obj, 'json': regular_json_obj})

if __name__ == '__main__':
    app.run(debug=True)
