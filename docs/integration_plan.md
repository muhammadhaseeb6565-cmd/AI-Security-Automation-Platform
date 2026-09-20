# Integration Plan

## Module Connections
The modules are decoupled and communicate asynchronously via file-based message queues.

- **Data Ingestion** -> (writes to) -> `data/raw_logs.jsonl`
- `data/raw_logs.jsonl` -> (read by) -> **Threat Intel Enricher**
- **Threat Intel Enricher** -> (writes to) -> `data/enriched_logs.jsonl`
- `data/enriched_logs.jsonl` -> (read by) -> **ML Detector**
- **ML Detector** -> (writes to) -> `data/alerts.jsonl`
- `data/alerts.jsonl` -> (read by) -> **SOAR Engine** & **Dashboard**

## Configuration Management
All thresholds, file paths, and mode flags are managed centrally in `config.yaml`. This ensures that any module can be reconfigured without changing the underlying Python code.

## Scalability Approach (Future Production)
For a production environment, the following integrations would be upgraded:
1. **Queues**: Replace JSONL files with Apache Kafka or RabbitMQ.
2. **Storage**: Store final alerts and metrics in Elasticsearch or a time-series database (InfluxDB) rather than flat files.
3. **Deployment**: Containerize each module using Docker and orchestrate them with Kubernetes, allowing independent scaling (e.g., scaling up the ML Detector if log volume spikes).
