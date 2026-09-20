import streamlit as st
import pandas as pd
import json
import yaml
import time
import os
import plotly.express as px

st.set_page_config(page_title="AI Security Platform", layout="wide", page_icon="shield")

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
alerts_file = config['queues']['alerts']

st.title("AI Security Automation Platform")
st.markdown("Real-time Threat Detection and Orchestration Dashboard")

# Initialize session state for holding alerts
if 'alerts_df' not in st.session_state:
    st.session_state.alerts_df = pd.DataFrame()

def load_alerts():
    if not os.path.exists(alerts_file):
        return pd.DataFrame()
        
    alerts = []
    with open(alerts_file, 'r') as f:
        for line in f:
            try:
                alerts.append(json.loads(line))
            except:
                pass
    return pd.DataFrame(alerts)

# Dashboard Layout
col1, col2, col3 = st.columns(3)

placeholder = st.empty()

while True:
    df = load_alerts()
    
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp', ascending=False)
        
        with placeholder.container():
            # Metrics
            high_risk = len(df[df['combined_risk_score'] >= config['thresholds']['high_confidence']])
            medium_risk = len(df[(df['combined_risk_score'] >= config['thresholds']['medium_confidence']) & (df['combined_risk_score'] < config['thresholds']['high_confidence'])])
            
            col1.metric("Total Events Analyzed", len(df))
            col2.metric("High Confidence Alerts", high_risk, delta_color="inverse")
            col3.metric("Medium Confidence Alerts", medium_risk, delta_color="inverse")
            
            st.divider()
            
            # Layout
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.subheader("Live Alert Feed")
                display_cols = ['timestamp', 'source_ip', 'destination_domain', 'ml_prediction', 'ti_risk_score', 'combined_risk_score']
                
                # Format dataframe for display
                display_df = df[display_cols].head(15).copy()
                display_df['Risk Level'] = display_df['combined_risk_score'].apply(
                    lambda x: 'High' if x >= config['thresholds']['high_confidence'] else ('Medium' if x >= config['thresholds']['medium_confidence'] else 'Low')
                )
                
                st.dataframe(display_df, use_container_width=True)
                
            with c2:
                st.subheader("Threat Intelligence")
                if 'combined_risk_score' in df.columns:
                    fig = px.histogram(df, x='combined_risk_score', title="Risk Score Distribution", 
                                       color_discrete_sequence=['indianred'])
                    st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Anomaly vs Normal")
                if 'ml_prediction' in df.columns:
                    pie_data = df['ml_prediction'].value_counts().reset_index()
                    pie_data.columns = ['Status', 'Count']
                    pie_data['Status'] = pie_data['Status'].map({1: 'Normal', -1: 'Anomaly'})
                    fig2 = px.pie(pie_data, values='Count', names='Status', title="ML Detections")
                    st.plotly_chart(fig2, use_container_width=True)
    else:
        with placeholder.container():
            st.info("Waiting for data. Start the platform to see live updates.")
            
    time.sleep(2)
