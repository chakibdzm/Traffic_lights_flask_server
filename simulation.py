import requests
import time
import random

def simulate_traffic_data():
    url = "http://localhost:5000/api/traffic_data"
    headers = {"Content-Type": "application/json"}

    while True:
        road_1_count = random.randint(0, 100)
        road_2_count = random.randint(0, 100)
        data = {
            "road_1": {"car_count": road_1_count},
            "road_2": {"car_count": road_2_count}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Data posted successfully: {data}")
        else:
            print(f"Failed to post data: {response.text}")

        time.sleep(5)  # Post data every 5 seconds

if __name__ == "__main__":
    simulate_traffic_data()
