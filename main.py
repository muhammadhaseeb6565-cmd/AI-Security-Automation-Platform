import argparse
import subprocess
import time
import os
import sys

def check_files():
    # Make sure we have the required directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Generate model if it doesn't exist
    if not os.path.exists('models/if_model.joblib'):
        print("Model not found. Generating mock Isolation Forest model...")
        subprocess.run([sys.executable, "generate_model.py"])
        
    # Clear old data files to start fresh for demo
    for f in ['data/raw_logs.jsonl', 'data/enriched_logs.jsonl', 'data/alerts.jsonl', 'data/ti_cache.json']:
        if os.path.exists(f):
            os.remove(f)

def start_module(script_name, name):
    print(f"Starting {name} ({script_name})...")
    if script_name == "dashboard.py":
        return subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_name, "--server.port=8501", "--server.headless=true"])
    return subprocess.Popen([sys.executable, script_name])

def run_full():
    print("="*50)
    print("Starting AI Security Automation Platform")
    print("="*50)
    
    check_files()
    
    processes = []
    try:
        # Start Dashboard first
        processes.append(start_module("dashboard.py", "Visualization Dashboard"))
        time.sleep(2)
        
        # Start SOAR
        processes.append(start_module("soar_engine.py", "SOAR Engine"))
        
        # Start ML Detector
        processes.append(start_module("ml_detector.py", "ML Detection Engine"))
        
        # Start TI Enricher
        processes.append(start_module("ti_enricher.py", "Threat Intel Enricher"))
        
        # Start Data Ingestion (generates logs)
        processes.append(start_module("ingest_logs.py", "Data Ingestion Layer"))
        
        print("\nAll modules running. Press Ctrl+C to stop.")
        print("View Dashboard at: http://localhost:8501\n")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down platform...")
        for p in processes:
            p.terminate()
        print("Platform stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Security Automation Platform")
    parser.add_argument("--mode", choices=["full"], default="full", help="Run mode")
    args = parser.parse_args()
    
    if args.mode == "full":
        run_full()
