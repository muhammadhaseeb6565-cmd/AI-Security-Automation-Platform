import json
import time
import os
import yaml
import hashlib

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

class ThreatIntelEnricher:
    def __init__(self, config):
        self.config = config
        self.cache_file = config['threat_intel']['cache_file']
        self.cache = self._load_cache()
        self.mock_mode = config['threat_intel']['mock_mode']
        
    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f)

    def _mock_query_ti(self, indicator, indicator_type):
        """Simulate TI query and return a mock risk score"""
        # Deterministic risk based on string hash
        hash_val = int(hashlib.md5(indicator.encode()).hexdigest(), 16)
        
        # Hardcode some known bad indicators for demonstration
        known_bad = ["185.15.59.224", "malicious-site.net", "suspicious.org"]
        if indicator in known_bad:
            return 0.95 # High risk
            
        known_good = ["8.8.8.8", "google.com", "192.168.1.10", "10.0.0.5", "example.com"]
        if indicator in known_good:
            return 0.05 # Low risk
            
        # Random but deterministic risk for others
        return (hash_val % 100) / 100.0

    def get_risk_score(self, indicator, indicator_type):
        if indicator in self.cache:
            return self.cache[indicator]
            
        if self.mock_mode:
            risk_score = self._mock_query_ti(indicator, indicator_type)
        else:
            # Placeholder for actual API call (e.g., requests.get to OTX)
            risk_score = 0.0 
            
        self.cache[indicator] = risk_score
        self._save_cache()
        return risk_score

    def enrich(self, log_entry):
        ip_risk = self.get_risk_score(log_entry['source_ip'], 'ip')
        domain_risk = self.get_risk_score(log_entry.get('destination_domain', ''), 'domain')
        
        # Combine risk scores
        overall_ti_risk = max(ip_risk, domain_risk)
        
        enriched_log = log_entry.copy()
        enriched_log['ti_risk_score'] = overall_ti_risk
        enriched_log['ti_enriched'] = True
        return enriched_log

def process_logs():
    config = load_config()
    raw_logs_file = config['queues']['raw_logs']
    enriched_logs_file = config['queues']['enriched_logs']
    
    enricher = ThreatIntelEnricher(config)
    last_pos = 0
    
    print("Starting Threat Intel Enricher...")
    
    while True:
        if os.path.exists(raw_logs_file):
            with open(raw_logs_file, "r") as f:
                f.seek(last_pos)
                lines = f.readlines()
                last_pos = f.tell()
                
                if lines:
                    with open(enriched_logs_file, "a") as out_f:
                        for line in lines:
                            try:
                                log = json.loads(line)
                                enriched_log = enricher.enrich(log)
                                out_f.write(json.dumps(enriched_log) + "\n")
                                print(f"[TI Enricher] Processed IP: {log['source_ip']}, Risk: {enriched_log['ti_risk_score']:.2f}")
                            except json.JSONDecodeError:
                                pass
        time.sleep(1)

if __name__ == "__main__":
    process_logs()
