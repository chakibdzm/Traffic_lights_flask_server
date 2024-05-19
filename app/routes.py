from flask import Blueprint, request, jsonify, render_template
import datetime

main = Blueprint('main', __name__)

traffic_data_store = {
    "road_1": [],
    "road_2": []
}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/traffic_data', methods=['POST'])
def traffic_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    timestamp = datetime.datetime.now().isoformat()
    if "road_1" in data:
        traffic_data_store["road_1"].append({"time": timestamp, "count": data["road_1"]["car_count"]})
    if "road_2" in data:
        traffic_data_store["road_2"].append({"time": timestamp, "count": data["road_2"]["car_count"]})

    return jsonify({"message": "Data received successfully"}), 200

@main.route('/api/traffic_chart_data', methods=['GET'])
def traffic_chart_data():
    return jsonify(traffic_data_store)
