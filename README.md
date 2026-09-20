# AI Security Automation Platform

A complete end-to-end security automation platform integrating Threat Intelligence, Machine Learning Anomaly Detection, SOAR orchestration, and real-time visualization.

## Modules

1. **Data Ingestion** (`ingest_logs.py`): Simulates streaming log ingestion.
2. **Threat Intelligence** (`ti_enricher.py`): Enriches logs with mock risk scores (simulating OTX/AbuseIPDB).
3. **ML Detection** (`ml_detector.py`): Uses an Isolation Forest model to detect anomalies based on session features.
4. **SOAR Engine** (`soar_engine.py`): Orchestrates playbooks for high/medium confidence alerts.
5. **Dashboard** (`dashboard.py`): Real-time Streamlit visualization.

## Setup & Running

### Requirements
Ensure you have Python 3.8+ installed. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Platform
To run the fully integrated platform:
```bash
python main.py --mode full
```

This will automatically:
1. Generate a mock ML model (if not present).
2. Start the Streamlit Dashboard (accessible at `http://localhost:8501`).
3. Start the SOAR, ML, and TI modules.
4. Begin ingesting simulated logs.

### Architecture Documentation
Please review the `docs/` folder for architectural diagrams, data flow, tech stack justification, and integration plans.
