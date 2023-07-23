from prometheus_client import start_http_server, Summary
from prometheus_client.core import CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector
import random
import time

import requests

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t: float):
    """A dummy function that takes some time."""
    time.sleep(t)

class CustomCollector(Collector):
    def collect(self):
        print("USGS Data Being Scraped...")
        c = CounterMetricFamily('usgs_total_earthquakes', 'Help text', labels=['time'])
        response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")
        response_json = response.json()
        earthquakes_list = response_json["features"]
        c.add_metric(['hourly'], len(earthquakes_list))
        yield c

REGISTRY.register(CustomCollector())

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())