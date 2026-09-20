import json
import time
import random
import os
import yaml
from datetime import datetime

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def generate_mock_log():
    """Simulates incoming logs (e.g., firewall, web server, syslogs)"""
    ips = ["192.168.1.10", "10.0.0.5", "8.8.8.8", "185.15.59.224", "45.33.32.156"]
    domains = ["example.com", "google.com", "malicious-site.net", "suspicious.org"]
    
    # Occasional malicious looking values
    is_malicious = random.random() < 0.1
    
    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": random.choice(ips) if not is_malicious else "185.15.59.224", # Malicious IP
        "destination_domain": random.choice(domains) if not is_malicious else "malicious-site.net",
        "bytes_sent": random.randint(100, 1000) if not is_malicious else random.randint(5000, 20000),
        "bytes_received": random.randint(1000, 10000) if not is_malicious else random.randint(50000, 200000),
        "failed_logins": random.randint(0, 1) if not is_malicious else random.randint(3, 10),
        "session_duration": random.randint(60, 600) if not is_malicious else random.randint(5, 30),
        "event_type": "network_traffic"
    }

def ingest_logs():
    config = load_config()
    raw_logs_file = config['queues']['raw_logs']
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(raw_logs_file), exist_ok=True)
    
    print("Starting data ingestion simulator...")
    try:
        while True:
            log_entry = generate_mock_log()
            # Append to raw logs queue (simulated as JSONL file)
            with open(raw_logs_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            print(f"[Ingest] Log ingested: {log_entry['source_ip']} -> {log_entry['destination_domain']}")
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("Ingestion stopped.")

if __name__ == "__main__":
    ingest_logs()
