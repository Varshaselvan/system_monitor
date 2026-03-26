# 🧠 AI-Based Silent Performance Degradation Detection System

## 📌 Overview

This project presents an **AI-based system for detecting silent performance degradation in computer systems** using **unsupervised machine learning and multivariate time-series analysis**.

Traditional monitoring systems rely on thresholds and reactive alerts, which often fail to detect gradual or hidden performance issues. This project introduces a **proactive and intelligent monitoring framework** that identifies early degradation, analyzes root causes, and provides actionable insights.

---

## 🎯 Problem Statement

Modern systems use:

* Threshold-based monitoring
* Rule-based alerts
* Log analysis tools

However, these approaches:

* Miss gradual degradation
* React only after failures occur
* Generate false or delayed alerts

👉 This project solves these limitations using **AI-driven anomaly detection**.

---

## 🎯 Objectives

* Detect early performance degradation using time-series analysis
* Analyze multivariate system metrics (CPU, memory, disk, network)
* Identify hidden performance drift without explicit failures
* Provide explainable insights using machine learning
* Reduce false positives in alert systems
* Enable proactive system maintenance

---

## 🚀 Key Features

* 🔐 User Authentication & Role Management
* 📊 Real-Time System Monitoring Dashboard
* 🤖 AI-Based Anomaly Detection (Unsupervised Learning)
* 🧠 Root Cause Analysis using Explainable AI (SHAP)
* 📈 Multivariate Time-Series Analysis
* 📧 Email Alerts & Notifications
* 🖥️ Server/System Management
* 💡 Recommendation Engine for Issue Resolution

---

## 🧩 System Modules

1. **System Degradation Analyzer** – Central monitoring platform
2. **System User** – Authentication and access control
3. **Server Management** – Register and manage systems
4. **Model Development** – ML model training and deployment
5. **Monitoring Agent** – Collects real-time system metrics
6. **Anomaly Detection** – Detects abnormal behavior
7. **Recommendation Engine** – Suggests corrective actions
8. **Alerts & Notifications** – Sends alerts via dashboard and email

---

## 🏗️ System Architecture

### 🔹 Existing System

* Threshold-based monitoring
* Reactive alerts
* Limited predictive capability

### 🔹 Proposed System

* AI-driven anomaly detection
* Continuous monitoring with agents
* Explainable ML insights
* Proactive alerting system

---

## ⚙️ Tech Stack

### 🖥️ Backend

* Python (Flask)
* Pandas, NumPy
* Scikit-learn
* PyTorch / TensorFlow

### 🌐 Frontend

* HTML, CSS, Bootstrap
* JavaScript

### 🗄️ Database

* MySQL

### 📦 Tools & Libraries

* SHAP (Explainable AI)
* Flask-Mail (Email Alerts)

---

## 🤖 Machine Learning Approach

* Uses **Unsupervised Learning**
* Based on **Multivariate Time-Series Analysis**
* Implements **GRU-VAE / OmniAnomaly-like models**
* Detects anomalies using **reconstruction error**
* Provides explainability using **SHAP values**

---

## 🔄 Workflow

1. Monitoring agent collects system metrics
2. Data is preprocessed and structured as time-series
3. ML model analyzes patterns and detects anomalies
4. System calculates anomaly scores
5. Root cause is identified using explainable AI
6. Alerts and recommendations are generated

---

## 📂 Project Structure

```bash
project/
│── app.py                 # Main Flask application
│── agent.py               # Monitoring agent
│── model/                 # ML models
│── database/              # SQL files
│── templates/             # HTML pages
│── static/                # CSS, JS, assets
│── utils/                 # Helper functions
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/project-name.git
cd project-name
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Database

```sql
CREATE DATABASE system_monitor;
```

Import the provided SQL file.

---

### 4️⃣ Configure Environment

Update email credentials in `app.py`:

```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

---

### 5️⃣ Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🧪 Testing

* Tested with real-time and historical data
* Validated CPU, memory, disk, and network monitoring
* Evaluated anomaly detection accuracy
* Tested under varying system loads
* Ensured low false positives

---

## 📊 Results

* ✅ Early detection of performance degradation
* ✅ Accurate anomaly detection using ML
* ✅ Reduced false alerts
* ✅ Clear root cause identification
* ✅ Improved system reliability and uptime

---

## 🔮 Future Enhancements

* ☁️ Cloud integration (AWS, Azure, GCP)
* ⚡ Real-time streaming analytics
* 🔄 Automated self-healing systems
* 📊 Advanced visualization dashboards

---

## 🔒 Security Notes

* Use environment variables for sensitive data
* Do not expose credentials publicly
* Implement role-based access control

---

## 👩‍💻 Authors

* Subitha G
* Swethalashmi G
* Varshaa S R

---

## 🎓 Academic Context

Developed as part of a **Computer Science and Engineering academic project** under the guidance of:

* Ms. Shahina Shalu S

---

## 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software with proper attribution.

See the LICENSE file for more details.

---

## ⭐ Acknowledgement

If you found this project useful, consider giving it a ⭐ on GitHub!
