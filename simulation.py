import requests
import json
import random
import time


url = 'http://127.0.0.1:5000/api/traffic_data'

def generate_traffic_data():
   
    road_1_count = random.randint(0, 20)
    road_2_count = random.randint(0, 20)

  
    traffic_data = {
        "road_1": {
            "car_count": road_1_count,
            "light_status": "green" 
        },
        "road_2": {
            "car_count": road_2_count,
            "light_status": "red" 
        }
    }
    return traffic_data

def send_data(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}, Response: {response.json()}")

if __name__ == "__main__":
    while True:
 
        traffic_data = generate_traffic_data()
        send_data(traffic_data)
        time.sleep(5) 
