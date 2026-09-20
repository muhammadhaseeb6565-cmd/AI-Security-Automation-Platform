import json
import time
import os
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def execute_playbook(alert, level):
    if level == "high":
        print(f"\n[SOAR] [HIGH CONFIDENCE ALERT]: {alert['source_ip']}")
        print(f"[SOAR] Executing Playbook: Block-IP")
        print(f"[SOAR] Action: Added {alert['source_ip']} to firewall blocklist.")
        print(f"[SOAR] Action: Sent notification to SOC team.\n")
    elif level == "medium":
        print(f"\n[SOAR] [MEDIUM CONFIDENCE ALERT]: {alert['source_ip']}")
        print(f"[SOAR] Executing Playbook: Analyst-Review")
        print(f"[SOAR] Action: Created JIRA Ticket #SEC-{int(time.time())}")
        print(f"[SOAR] Action: Added to analyst queue for manual review.\n")

def process_alerts():
    config = load_config()
    alerts_file = config['queues']['alerts']
    
    threshold_high = config['thresholds']['high_confidence']
    threshold_medium = config['thresholds']['medium_confidence']
    
    last_pos = 0
    print("Starting SOAR Orchestration Engine...")
    
    while True:
        if os.path.exists(alerts_file):
            with open(alerts_file, "r") as f:
                f.seek(last_pos)
                lines = f.readlines()
                last_pos = f.tell()
                
                if lines:
                    for line in lines:
                        try:
                            alert = json.loads(line)
                            risk = alert.get('combined_risk_score', 0)
                            
                            if risk >= threshold_high:
                                execute_playbook(alert, "high")
                            elif risk >= threshold_medium:
                                execute_playbook(alert, "medium")
                            # Low risk is ignored by SOAR
                            
                        except json.JSONDecodeError:
                            pass
        time.sleep(1)

if __name__ == "__main__":
    process_alerts()
