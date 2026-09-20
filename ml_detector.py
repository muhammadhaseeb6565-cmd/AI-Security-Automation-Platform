import json
import time
import os
import yaml
import joblib
import pandas as pd

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def process_logs():
    config = load_config()
    enriched_logs_file = config['queues']['enriched_logs']
    alerts_file = config['queues']['alerts']
    model_path = config['models']['isolation_forest']
    
    print(f"Loading ML model from {model_path}...")
    try:
        model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}. Please run generate_model.py first.")
        return

    last_pos = 0
    print("Starting ML Detector...")
    
    features = ['bytes_sent', 'bytes_received', 'failed_logins', 'session_duration']
    
    while True:
        if os.path.exists(enriched_logs_file):
            with open(enriched_logs_file, "r") as f:
                f.seek(last_pos)
                lines = f.readlines()
                last_pos = f.tell()
                
                if lines:
                    with open(alerts_file, "a") as out_f:
                        for line in lines:
                            try:
                                log = json.loads(line)
                                
                                # Extract features
                                df = pd.DataFrame([log], columns=features)
                                
                                # Predict anomaly (-1 for outliers, 1 for inliers)
                                prediction = model.predict(df)[0]
                                
                                # Anomaly score (lower is more abnormal)
                                anomaly_score = model.score_samples(df)[0]
                                
                                # Normalize anomaly score to 0-1 risk scale roughly (heuristic for demo)
                                # Isolation Forest scores are negative, where smaller values are more anomalous
                                ml_risk_score = min(1.0, max(0.0, abs(anomaly_score) * 2))
                                
                                log['ml_prediction'] = int(prediction)
                                log['ml_risk_score'] = float(ml_risk_score)
                                
                                # Combine ML and TI risk
                                combined_risk = (log.get('ti_risk_score', 0) * 0.4) + (ml_risk_score * 0.6)
                                log['combined_risk_score'] = combined_risk
                                
                                # Output to alerts queue
                                out_f.write(json.dumps(log) + "\n")
                                print(f"[ML Detector] Analysed IP: {log['source_ip']}, ML Risk: {ml_risk_score:.2f}, Combined: {combined_risk:.2f}")
                                
                            except json.JSONDecodeError:
                                pass
                            except KeyError as e:
                                print(f"Missing key in log: {e}")
        time.sleep(1)

if __name__ == "__main__":
    process_logs()
