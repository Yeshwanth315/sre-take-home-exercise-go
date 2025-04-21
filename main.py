import json
import logging
import math
import os
import requests
import time
import yaml

# Setting up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class Endpoint:
    def __init__(self, name, url, method=None, headers=None, body=None):
        self.name = name
        self.url = url
        self.method = method or "GET"  # Default to GET if method is not provided
        self.headers = headers or {}   # Default to empty dict if headers are not provided
        self.body = body or {}         # Default to empty dict if body is not provided

class DomainStats:
    def __init__(self):
        self.success = 0
        self.total = 0

stats = {}

def check_health(endpoint):
    global stats

    try:
        body = json.dumps(endpoint.__dict__) if endpoint.body else None
        req = requests.Request(endpoint.method, endpoint.url, data=body, headers=endpoint.headers)
        prepared = req.prepare()
        session = requests.Session()

        start = time.time()
        response = session.send(prepared, timeout=0.5)

        elapsed = (time.time() - start) * 1000  # Convert to milliseconds

        domain = extract_domain(endpoint.url)

        if domain not in stats:
            stats[domain] = DomainStats()

        stats[domain].total += 1

        if response.status_code >= 200 and response.status_code < 300 and elapsed <= 500:
            stats[domain].success += 1
        elif elapsed > 500:
            logging.warning(f"⚠️ {endpoint.name} took too long to respond: {int(elapsed)}ms")

    except requests.exceptions.Timeout:
        logging.warning(f"⏱️ {endpoint.name} timed out (>{500}ms)")
    except Exception as e:
        logging.error(f"❌ Error checking health for {endpoint.name}: {e}")

def extract_domain(url):
    url_split = url.split("//")
    domain = url_split[-1].split("/")[0]
    return domain

def monitor_endpoints(endpoints):
    global stats

    for endpoint in endpoints:
        domain = extract_domain(endpoint.url)
        if domain not in stats:
            stats[domain] = DomainStats()

    while True:
        cycle_start = time.time()  # ⏱️ Start of cycle
        
        for endpoint in endpoints:
            check_health(endpoint)
        log_results()    # 📊 Log availability results

        #💤 Sleep to maintain fixed 15-second cycles
        elapsed = time.time() - cycle_start
        sleep_duration = max(0, 15 - elapsed)
        time.sleep(sleep_duration)

def log_results():
    for domain, stat in stats.items():
        if stat.total == 0:
            percentage = 0
        else:
            percentage = round(100 * stat.success / stat.total)

        # message = f"{domain} has {percentage}% availability"
        message = (
            f"{domain} - {percentage}% availability "
            f"({stat.success} successful / {stat.total} total requests)"
        )
        print(message)
        logging.info(message)  # Optional: logs to file or console if logging is configured

def main():
    if len(os.sys.argv) < 2:
        logging.error("Usage: python main.py <config_file>")
        return

    file_path = os.sys.argv[1]
    try:
        with open(file_path, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
        return

    try:
        endpoints = yaml.safe_load(data)
        endpoint_objects = [Endpoint(**ep) for ep in endpoints]

        try:
            monitor_endpoints(endpoint_objects)
        except KeyboardInterrupt:
            log_results()  # Optional: log final stats before exit
            logging.info("🛑 Gracefully stopped by user (Ctrl+C)")
            exit(0)  # Gracefully exit the program
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        
if __name__ == "__main__":
    main()
