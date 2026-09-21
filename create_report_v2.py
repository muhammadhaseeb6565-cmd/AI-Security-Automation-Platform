import os
from docx import Document
from docx.shared import Inches, Pt
from fpdf import FPDF

def create_comprehensive_word_report():
    doc = Document()
    
    # Title
    title = doc.add_heading('AI Security Automation Platform', 0)
    title.alignment = 1 # Center
    
    subtitle = doc.add_paragraph('Comprehensive Capstone Project Report\nAdvanced AI, Automation & Security Engineering Track\n')
    subtitle.alignment = 1
    
    # 1. Executive Summary
    doc.add_heading('1. Executive Summary', level=1)
    doc.add_paragraph(
        "This comprehensive report details the end-to-end design, implementation, and evaluation of the "
        "AI Security Automation Platform developed for the Week 10 Final Capstone. The platform integrates "
        "threat intelligence, machine learning anomaly detection, SOAR (Security Orchestration, Automation, and Response) "
        "orchestration, and real-time visualization into a unified, production-ready system."
    )
    
    # 2. Project Objectives
    doc.add_heading('2. Project Objectives', level=1)
    doc.add_paragraph("The primary objectives of this capstone project were to:", style='List Bullet')
    doc.add_paragraph("Build a modular data ingestion layer capable of normalizing raw security logs.", style='List Bullet')
    doc.add_paragraph("Enrich incoming log data with threat intelligence risk scores.", style='List Bullet')
    doc.add_paragraph("Deploy a machine learning model to detect behavioral anomalies in real-time.", style='List Bullet')
    doc.add_paragraph("Implement a SOAR engine to automatically execute defensive playbooks for high-confidence threats.", style='List Bullet')
    doc.add_paragraph("Provide analysts with a real-time, interactive security dashboard.", style='List Bullet')
    
    # 3. System Architecture
    doc.add_heading('3. System Architecture (Deep Dive)', level=1)
    doc.add_paragraph(
        "The platform utilizes a highly modular, decoupled microservice architecture where each component operates "
        "independently, communicating asynchronously via file-based JSONL message queues. This ensures graceful "
        "degradation and ease of testing."
    )
    
    doc.add_heading('3.1 Data Ingestion Layer', level=2)
    doc.add_paragraph(
        "Implemented in `ingest_logs.py`, this module simulates streaming log ingestion from network devices. "
        "It generates normalized JSON payloads containing source IP, destination domain, byte transfers, and session data, "
        "which are then written to the `raw_logs.jsonl` queue."
    )
    
    doc.add_heading('3.2 Threat Intelligence Enrichment', level=2)
    doc.add_paragraph(
        "Implemented in `ti_enricher.py`, this module tails the raw logs and queries a mock Threat Intelligence API "
        "(simulating AlienVault OTX or AbuseIPDB). It uses MD5 hashing to generate deterministic risk scores for IPs and domains, "
        "caches the results for performance, and outputs to `enriched_logs.jsonl`."
    )
    
    doc.add_heading('3.3 Machine Learning Detection', level=2)
    doc.add_paragraph(
        "Implemented in `ml_detector.py`, this module applies an Isolation Forest model to detect network anomalies. "
        "The model evaluates bytes sent/received, failed logins, and session duration. The ML anomaly score is combined "
        "with the TI risk score to produce a final `combined_risk_score`."
    )
    
    doc.add_heading('3.4 SOAR Orchestration', level=2)
    doc.add_paragraph(
        "Implemented in `soar_engine.py`, this engine acts on the final alerts. High-confidence alerts (score >= 0.8) "
        "trigger automated playbooks (e.g., firewall blocklist automation), while medium-confidence alerts (score >= 0.5) "
        "are queued for human-in-the-loop analyst review (e.g., JIRA ticketing)."
    )
    
    doc.add_heading('3.5 Visualization Dashboard', level=2)
    doc.add_paragraph(
        "Implemented in `dashboard.py` using Streamlit, this frontend provides real-time visibility into the platform's operations. "
        "It features live alert feeds, threat intelligence metric counters, and Plotly-based interactive charts."
    )
    
    # 4. Technical Stack
    doc.add_heading('4. Technical Stack & Implementation Details', level=1)
    doc.add_paragraph("Language: Python 3", style='List Bullet')
    doc.add_paragraph("Machine Learning: scikit-learn (Isolation Forest), pandas, joblib", style='List Bullet')
    doc.add_paragraph("Visualization: Streamlit, Plotly Express", style='List Bullet')
    doc.add_paragraph("Configuration & Data: YAML (config.yaml), JSONL (mock message queues)", style='List Bullet')
    
    doc.add_heading('5. Engineering Review & Reflection', level=1)
    
    p1 = doc.add_paragraph()
    p1.add_run("What worked well:").bold = True
    doc.add_paragraph("Decoupling the modules using intermediate queues allowed each component to be developed and tested independently. The Streamlit dashboard seamlessly integrated by simply reading the final alerts queue.")
    
    p2 = doc.add_paragraph()
    p2.add_run("What would you do differently:").bold = True
    doc.add_paragraph("For a true production environment, I would replace the file-based queues with Apache Kafka or RabbitMQ, and utilize Docker Compose to orchestrate the services.")
    
    p3 = doc.add_paragraph()
    p3.add_run("Performance & Scalability:").bold = True
    doc.add_paragraph("The platform processes events sub-millisecond per log due to the lightweight mock API and efficient Isolation Forest model. To scale 10x, deploying Kubernetes pods for horizontal scaling of the ML and TI workers would be required.")
    
    p4 = doc.add_paragraph()
    p4.add_run("Security Vulnerabilities:").bold = True
    doc.add_paragraph("Current vulnerabilities include lack of dashboard authentication, on-disk plaintext JSONL queues susceptible to tampering, and the need for a secure secrets manager (e.g., AWS Secrets Manager) for real TI API keys.")
    
    # 6. Demo Screenshots
    doc.add_heading('6. Demo Screenshots', level=1)
    images = ["p1.PNG", "p2.PNG", "p3.PNG", "p4.PNG"]
    for img in images:
        if os.path.exists(img):
            doc.add_paragraph(f"Figure: {img}")
            doc.add_picture(img, width=Inches(6.0))
            
    doc.save('Comprehensive_Detailed_Report.docx')
    print("Created Comprehensive_Detailed_Report.docx")

def create_comprehensive_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "AI Security Automation Platform", ln=True, align='C')
    pdf.set_font("Arial", 'I', 14)
    pdf.cell(0, 10, "Comprehensive Capstone Project Report", ln=True, align='C')
    pdf.ln(10)
    
    def add_section(title, text):
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, text)
        pdf.ln(5)
        
    def add_subsection(title, text):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, text)
        pdf.ln(3)

    add_section("1. Executive Summary", "This comprehensive report details the end-to-end design, implementation, and evaluation of the AI Security Automation Platform developed for the Week 10 Final Capstone. The platform integrates threat intelligence, machine learning anomaly detection, SOAR (Security Orchestration, Automation, and Response) orchestration, and real-time visualization into a unified, production-ready system.")
    
    add_section("2. Project Objectives", "The primary objectives of this capstone project were to:\n- Build a modular data ingestion layer capable of normalizing raw security logs.\n- Enrich incoming log data with threat intelligence risk scores.\n- Deploy a machine learning model to detect behavioral anomalies in real-time.\n- Implement a SOAR engine to automatically execute defensive playbooks.\n- Provide analysts with a real-time, interactive security dashboard.")
    
    add_section("3. System Architecture (Deep Dive)", "The platform utilizes a highly modular, decoupled microservice architecture where each component operates independently, communicating asynchronously via file-based JSONL message queues.")
    
    add_subsection("3.1 Data Ingestion Layer", "Implemented in ingest_logs.py, this module simulates streaming log ingestion from network devices. It generates normalized JSON payloads containing source IP, destination domain, byte transfers, and session data.")
    add_subsection("3.2 Threat Intelligence Enrichment", "Implemented in ti_enricher.py, this module tails the raw logs and queries a mock Threat Intelligence API. It uses MD5 hashing to generate deterministic risk scores for IPs and domains.")
    add_subsection("3.3 Machine Learning Detection", "Implemented in ml_detector.py, this module applies an Isolation Forest model to detect network anomalies. The model evaluates bytes sent/received, failed logins, and session duration.")
    add_subsection("3.4 SOAR Orchestration", "Implemented in soar_engine.py, this engine acts on the final alerts. High-confidence alerts trigger automated playbooks, while medium-confidence alerts are queued for human review.")
    add_subsection("3.5 Visualization Dashboard", "Implemented in dashboard.py using Streamlit, this frontend provides real-time visibility into the platform's operations.")
    
    add_section("4. Technical Stack & Implementation Details", "- Language: Python 3\n- Machine Learning: scikit-learn (Isolation Forest), pandas, joblib\n- Visualization: Streamlit, Plotly Express\n- Configuration & Data: YAML (config.yaml), JSONL (mock message queues)")
    
    add_section("5. Engineering Review & Reflection", "What worked well:\nDecoupling the modules using intermediate queues allowed each component to be developed and tested independently.\n\nWhat would you do differently:\nFor a true production environment, I would replace the file-based queues with Apache Kafka or RabbitMQ, and utilize Docker Compose.\n\nPerformance & Scalability:\nThe platform processes events sub-millisecond per log. To scale 10x, deploying Kubernetes pods for horizontal scaling would be required.\n\nSecurity Vulnerabilities:\nCurrent vulnerabilities include lack of dashboard authentication, on-disk plaintext JSONL queues susceptible to tampering, and the need for a secure secrets manager.")
    
    # 6. Demo Screenshots
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "6. Demo Screenshots", ln=True)
    images = ["p1.PNG", "p2.PNG", "p3.PNG", "p4.PNG"]
    for img in images:
        if os.path.exists(img):
            pdf.ln(5)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 10, f"Figure: {img}", ln=True)
            pdf.image(img, w=170)
            
    pdf.output('Comprehensive_Detailed_Report.pdf')
    print("Created Comprehensive_Detailed_Report.pdf")

if __name__ == "__main__":
    create_comprehensive_word_report()
    create_comprehensive_pdf_report()
