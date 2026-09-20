import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

def generate_mock_model():
    print("Generating mock Isolation Forest model...")
    # Generate mock training data (normal behavior)
    # Features: bytes_sent, bytes_received, failed_logins, session_duration
    np.random.seed(42)
    normal_data = pd.DataFrame({
        'bytes_sent': np.random.normal(500, 100, 1000),
        'bytes_received': np.random.normal(5000, 1000, 1000),
        'failed_logins': np.random.poisson(0.1, 1000),
        'session_duration': np.random.normal(300, 50, 1000)
    })
    
    # Train Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(normal_data)
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model_path = 'models/if_model.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    generate_mock_model()
