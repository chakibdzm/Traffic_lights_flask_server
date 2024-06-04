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
        container.upsert_item({
            "id": f"road_1_{timestamp}",
            "road": "road_1",
            "time": timestamp,
            "count": data["road_1"]["car_count"]
        })
    if "road_2" in data:
        container.upsert_item({
            "id": f"road_2_{timestamp}",
            "road": "road_2",
            "time": timestamp,
            "count": data["road_2"]["car_count"]
        })

    return jsonify({"message": "Data received successfully"}), 200

@main.route('/api/traffic_chart_data', methods=['GET'])
def traffic_chart_data():
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    
    road_1_data = [item for item in items if item['road'] == 'road_1']
    road_2_data = [item for item in items if item['road'] == 'road_2']

    traffic_data_store = {
        "road_1": road_1_data,
        "road_2": road_2_data
    }
    
    return jsonify(traffic_data_store)
