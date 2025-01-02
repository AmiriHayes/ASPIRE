# this file is for the demo website: www.aspirefortransport.org

import osmnx
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    param1 = data.get('neighborhood_name')
    param2 = data.get('city_name')
    param3 = data.get('state_name')

    # processing logic:
    geojson_obj = {'testkey1': 'testval1'}
    regular_json_obj = {'testkey2': 'testval2'}

    return jsonify({'geojson': geojson_obj, 'json': regular_json_obj})

if __name__ == '__main__':
    app.run(debug=True)