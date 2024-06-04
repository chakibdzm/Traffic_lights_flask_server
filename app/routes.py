from flask import Blueprint, request, jsonify, render_template
import datetime
import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

main = Blueprint('main', __name__)

# Azure Cosmos DB configuration
COSMOS_URL = os.getenv('COSMOS_URL')
COSMOS_KEY = os.getenv('COSMOS_KEY')
DATABASE_NAME = 'TrafficDB'
CONTAINER_NAME = 'TrafficData'

# Initialize Cosmos client
client = CosmosClient(COSMOS_URL, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/road"),
    offer_throughput=400
)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/simulation')
def simulation():
    return render_template('simulation.html')

@main.route('/api/traffic_data', methods=['POST'])
def traffic_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    timestamp = datetime.datetime.now().isoformat()
    if "road_1" in data:
        road_1_data = data["road_1"]
        container.upsert_item({
            "id": f"road_1_{timestamp}",
            "road": "road_1",
            "time": timestamp,
            "count": road_1_data["car_count"],
            "green_time": road_1_data.get("green_time", None),
            "red_time": road_1_data.get("red_time", None)
        })
    if "road_2" in data:
        road_2_data = data["road_2"]
        container.upsert_item({
            "id": f"road_2_{timestamp}",
            "road": "road_2",
            "time": timestamp,
            "count": road_2_data["car_count"]
        })

    return jsonify({"message": "Data received successfully"}), 200


@main.route('/api/traffic_chart_data', methods=['GET'])
def traffic_chart_data():
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    
    road_1_data = [{
        "time": item['time'],
        "count": item['count'],
        "green_time": item.get('green_time', None),
        "red_time": item.get('red_time', None)
    } for item in items if item['road'] == 'road_1']
    
    road_2_data = [{
        "time": item['time'],
        "count": item['count']
    } for item in items if item['road'] == 'road_2']

    traffic_data_store = {
        "road_1": road_1_data,
        "road_2": road_2_data
    }
    
    return jsonify(traffic_data_store)


def fetch_traffic_data_from_cosmos():
    # Query Cosmos DB to fetch road 1 data
    query = "SELECT c.time, c.count, c.green_time, c.red_time FROM c WHERE c.road = 'road_1'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    road_1_data = []

    for item in items:
        road_1_item = {
            "time": item['time'],
            "count": item['count']
        }
        if 'green_time' in item:
            road_1_item['green_time'] = item['green_time']
        if 'red_time' in item:
            road_1_item['red_time'] = item['red_time']

        road_1_data.append(road_1_item)

    return road_1_data




@main.route('/traffic_data')
def traffic_data_view():
    # Assuming you have a function to fetch traffic data from Cosmos DB
    road_1_data = fetch_traffic_data_from_cosmos()  # Modify this to fetch Road 1 data

    return render_template('traffic_data.html', road1_data=road_1_data)

