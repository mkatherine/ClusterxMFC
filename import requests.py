import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone

# Define Prometheus API endpoint
PROMETHEUS_URL = "http://192.168.0.156:9090/api/v1/query_range"
METRICS = ["mqtt_voltage", "mqtt_temperature", "mqtt_moisture"]  # List of metrics to fetch

# Calculate the timestamps for 1 month ago and now
end_time = int(time.time())  # Current time in Unix timestamp
start_time = int((datetime.now() - timedelta(days=7)).timestamp())  # 1 month ago in Unix timestamp

# Initialize an empty list to store all results
all_results = []

# Fetch data for each metric
for metric in METRICS:
    # Construct the query for the current metric
    url = f"{PROMETHEUS_URL}?query={metric}&start={start_time}&end={end_time}&step=60"
    
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success' and data['data']['result']:
            # Process the data if available
            for result in data["data"]["result"]:
                metric_name = result["metric"]
                for value in result["values"]:
                    # Updated timestamp conversion using timezone.utc
                    timestamp = datetime.fromtimestamp(value[0], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    all_results.append({"metric": metric_name, "timestamp": timestamp, "value": value[1]})
        else:
            print(f"No data found for metric {metric}")
    else:
        print(f"Failed to fetch data for {metric}. Status Code: {response.status_code}")
        print("Error message:", response.text)


# Convert to CSV if any results are collected
if all_results:
    df = pd.DataFrame(all_results)
    df.to_csv(r"C:\Users\kathe\Desktop\MudWatts\prometheus_multiple_metrics.csv", index=False)
    print("Data saved as prometheus_multiple_metrics.csv")
else:
    print("No data collected for any metric.")
