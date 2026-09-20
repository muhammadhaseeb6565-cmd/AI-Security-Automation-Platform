# Data Flow Architecture

The data moves through the AI Security Platform in a linear pipeline via file-based message queues.

1. **Ingestion Layer (`ingest_logs.py`)**: 
   - Generates simulated JSON log entries.
   - Appends to `data/raw_logs.jsonl`.

2. **Threat Intelligence Layer (`ti_enricher.py`)**:
   - Tails `data/raw_logs.jsonl`.
   - Queries mock TI APIs to calculate IP and domain risk scores.
   - Appends enriched JSON payload to `data/enriched_logs.jsonl`.

3. **Machine Learning Layer (`ml_detector.py`)**:
   - Tails `data/enriched_logs.jsonl`.
   - Passes features (`bytes_sent`, `bytes_received`, `failed_logins`, `session_duration`) to the Isolation Forest model.
   - Calculates `ml_risk_score` and `combined_risk_score`.
   - Appends analyzed payload to `data/alerts.jsonl`.

4. **SOAR & Visualization Layer**:
   - **SOAR Engine (`soar_engine.py`)**: Tails `data/alerts.jsonl`, triggering playbooks if `combined_risk_score` exceeds thresholds.
   - **Dashboard (`dashboard.py`)**: Polls `data/alerts.jsonl` every 2 seconds to update real-time charts and metric counters.
