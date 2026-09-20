# Technology Stack

## 1. Programming Language
- **Python 3**: Chosen for its robust ecosystem in data science, cybersecurity, and rapid prototyping capabilities.

## 2. Machine Learning
- **scikit-learn**: Used for the `IsolationForest` model. It is lightweight, industry-standard, and perfect for tabular anomaly detection without the overhead of deep learning frameworks.
- **joblib**: Used for saving and loading the pre-trained model efficiently.

## 3. Data Processing
- **pandas**: Utilized for feature extraction and data manipulation before feeding data into the ML model.

## 4. Visualization
- **Streamlit**: Selected for the dashboard because it allows for rapid development of interactive, data-driven web applications natively in Python without needing HTML/JS.
- **Plotly Express**: Used for building interactive charts (histograms, pie charts) within Streamlit.

## 5. Message Queuing & Inter-Process Communication
- **JSONL (JSON Lines) files**: Used as lightweight, mock message queues (`raw_logs.jsonl`, `enriched_logs.jsonl`, `alerts.jsonl`). 
- *Justification*: While Redis or RabbitMQ are better for production, using append-only JSONL files allows the capstone to be run out-of-the-box by reviewers without requiring external database or broker installations, fulfilling the MVP requirements effectively.
