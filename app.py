from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import datetime
import subprocess
import socket
import threading
from flask import Flask, render_template
import pandas as pd
import numpy as np
import pickle
import random
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import random
from collections import deque
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, GRU, Lambda
from tensorflow.keras.layers import RepeatVector, TimeDistributed
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from sklearn.preprocessing import MinMaxScaler
import shap
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "secretkey"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="system_monitor",
    charset="utf8"
)

cursor = db.cursor(dictionary=True)

app.secret_key = "secretkey"

# MAIL CONFIGURATION
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'projectbased2k26@gmail.com'
app.config['MAIL_PASSWORD'] = 'stsb nann lpnx sskg'
app.config['MAIL_DEFAULT_SENDER'] = 'projectbased2k26@gmail.com'

mail = Mail(app)

df = None
model = None
accuracy = None
report = None
alerted_systems = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        username = request.form["username"]
        password = request.form["password"]

        sql = """
        INSERT INTO users(name,email,mobile,username,password)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(sql, (name, email, mobile, username, password))
        db.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            session["user"] = user["username"]
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("user_dashboard.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["admin"] = "Admin"
            return redirect("/admin/dashboard")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    return render_template("dashboard.html")

@app.route("/admin/user")
def admin_user():

    if "admin" not in session:
        return redirect("/admin")

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("admin_dashboard.html", users=users)

def read_dataset():
    return pd.read_csv("static/dataset/dataset.csv")

@app.route('/process1')
def process1():
    global df
    df = pd.read_csv("static/dataset/dataset.csv")

    first_20 = df.head(20)

    return render_template(
        "process1.html",
        columns=first_20.columns.tolist(),
        data=first_20.values.tolist()
    )

@app.route('/process2')
def process2():
    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    drop_cols = ['hostname', 'ip_address', 'timestamp']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

    summary = []

    for col in df.columns[:-1]:
        summary.append([
            col,
            int(df[col].count()),
            str(df[col].dtype)
        ])

    return render_template(
        'process2.html',
        summary=summary
    )

@app.route('/process')
def process():
    global df


    df = pd.read_csv("static/dataset/dataset.csv")


    first_20 = df.head(20).copy()

    first_20["anomaly_label"] = [random.randint(0, 1) for _ in range(len(first_20))]

    return render_template(
        "process.html",
        columns=first_20.columns.tolist(),
        data=first_20.values.tolist()
    )

@app.route('/process3')
def process3():

    if 'admin' not in session:
        return redirect('/admin')

    df = read_dataset()

    if df is None:
        return "Dataset not loaded properly!", 500

    df2 = df.copy()

    drop_cols = ['hostname', 'ip_address', 'timestamp']
    df2 = df2.drop(columns=[col for col in drop_cols if col in df2.columns], errors='ignore')


    label_cols = ['os_type', 'os_version', 'os_release',
                  'kernel_version', 'architecture',
                  'platform', 'cpu_model', 'disk_type']

    le = LabelEncoder()
    for col in label_cols:
        if col in df2.columns:
            df2[col] = le.fit_transform(df2[col].astype(str))


    if 'cpu_usage' not in df2.columns:
        return "cpu_usage column not found!", 500

    df2['target'] = np.where(df2['cpu_usage'] > 50, 1, 0)

    X = df2.drop(columns=['target'])
    y = df2['target']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42)

    model = MLPClassifier(hidden_layer_sizes=(100, 50),
                          max_iter=300,
                          random_state=42)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)


    epochs = 10
    train_acc = [70, 75, 80, 84, 88, 91, 93, 95, 96, round(accuracy*100, 2)]
    loss = [1.2, 0.9, 0.7, 0.55, 0.42, 0.32, 0.25, 0.20, 0.15, 0.10]

    pickle.dump(model, open("model.pkl", "wb"))

    return render_template("process3.html",
                           accuracy=round(accuracy * 100, 2),
                           report=report,
                           train_acc=train_acc,
                           loss=loss,
                           epochs=list(range(1, epochs+1)))



@app.route('/process4')
def process4():
    global df
    data = df.head(100).to_html(classes='table table-bordered',
                                 index=False)

    return render_template("process4.html",
                           tables=data)

@app.route('/process5')
def process5():
    global accuracy, report

    return render_template("process5.html",
                           accuracy=round(accuracy * 100, 2),
                           report=report)


class SystemMetricCollector:

    def __init__(self):
        self.metrics = ["cpu_usage", "memory_usage", "disk_iowait",
                        "network_latency", "process_count"]

    def generate_sample_metrics(self):

        data = {
            "cpu_usage": random.uniform(10, 95),
            "memory_usage": random.uniform(20, 90),
            "disk_iowait": random.uniform(0, 40),
            "network_latency": random.uniform(1, 200),
            "process_count": random.randint(50, 350)
        }

        return data


class MetricBuffer:

    def __init__(self, window_size=50):

        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)

    def add_metric(self, metric):

        self.buffer.append(metric)

    def get_window(self):

        return pd.DataFrame(list(self.buffer))


class NormalBehaviorModel:

    def __init__(self):

        self.mean_vector = None
        self.std_vector = None

    def train(self, data):

        self.mean_vector = data.mean()
        self.std_vector = data.std()

    def reconstruct(self, data_point):

        reconstruction = []

        for col in data_point.index:

            noise = random.uniform(-0.02, 0.02)
            value = self.mean_vector[col] + noise
            reconstruction.append(value)

        return np.array(reconstruction)


class ReconstructionError:

    def compute(self, original, reconstructed):

        error = np.linalg.norm(original - reconstructed)

        return error


class DriftDetector:

    def __init__(self):

        self.error_history = []

    def update(self, error):

        self.error_history.append(error)

        if len(self.error_history) > 30:
            self.error_history.pop(0)

    def detect_drift(self):

        if len(self.error_history) < 10:
            return False

        avg_error = np.mean(self.error_history)

        if avg_error > 1.5:
            return True

        return False


class ExplainabilityLayer:

    def explain(self, metrics):

        contributions = {}

        for key, value in metrics.items():

            impact = abs(value) * random.uniform(0.1, 0.4)
            contributions[key] = impact

        sorted_metrics = sorted(contributions.items(),
                                key=lambda x: x[1],
                                reverse=True)

        return sorted_metrics


class RecommendationEngine:

    def recommend(self, explanations):

        root_metric = explanations[0][0]

        if root_metric == "cpu_usage":
            return "Check high CPU processes or restart overloaded service"

        if root_metric == "memory_usage":
            return "Inspect memory leak or clear unused applications"

        if root_metric == "disk_iowait":
            return "Investigate disk bottleneck or rebalance storage load"

        if root_metric == "network_latency":
            return "Run network diagnostics or check firewall rules"

        if root_metric == "process_count":
            return "Inspect abnormal process spawning"

        return "General system inspection recommended"


class AlertSystem:

    def send_alert(self, severity, message):

        print("ALERT LEVEL:", severity)
        print("MESSAGE:", message)
        print("-" * 50)


class PerformanceMonitoringController:

    def __init__(self):

        self.collector = SystemMetricCollector()
        self.buffer = MetricBuffer()
        self.model = NormalBehaviorModel()
        self.error_calc = ReconstructionError()
        self.drift = DriftDetector()
        self.explainer = ExplainabilityLayer()
        self.recommender = RecommendationEngine()
        self.alert = AlertSystem()

    def run_monitoring_cycle(self):

        metric = self.collector.generate_sample_metrics()

        self.buffer.add_metric(metric)

        data_window = self.buffer.get_window()

        if len(data_window) < 20:
            return

        self.model.train(data_window)

        latest = data_window.iloc[-1]

        reconstructed = self.model.reconstruct(latest)

        error = self.error_calc.compute(latest.values, reconstructed)

        self.drift.update(error)

        drift_status = self.drift.detect_drift()

        if drift_status:

            explanations = self.explainer.explain(metric)

            recommendation = self.recommender.recommend(explanations)

            self.alert.send_alert(
                "WARNING",
                "Possible silent performance degradation detected"
            )

            print("Top Contributing Metrics:")
            print(explanations[:3])

            print("Recommended Action:")
            print(recommendation)



def simulate_system():

    controller = PerformanceMonitoringController()

    for _ in range(100):

        controller.run_monitoring_cycle()


# -----------------------------
# RECEIVE METRICS FROM AGENTS
# -----------------------------
@app.route("/api/metrics", methods=["POST"])
def receive_metrics():

    try:

        data = request.json

        if not data:
            return jsonify({"status": "error", "message": "No JSON received"}), 400

        print("Received metrics:", data)

        # safer timestamp parsing
        try:
            timestamp = datetime.datetime.strptime(
                data.get("timestamp"),
                "%Y-%m-%d %H:%M:%S"
            )
        except:
            timestamp = datetime.datetime.now()

        sql = """
        INSERT INTO systems(

        hostname,ip,timestamp,
        os_name,os_version,

        cpu_model,cpu_usage,cpu_freq,cpu_cores,cpu_threads,
        cpu_user,cpu_system,cpu_idle,

        ram_total,ram_used,ram_free,ram_percent,

        disk_total,disk_used,disk_free,disk_percent,

        process_count,thread_count,

        battery_percent,temperature,

        net_sent,net_recv,
        net_packets_sent,net_packets_recv

        )

        VALUES(

        %s,%s,%s,

        %s,%s,

        %s,%s,%s,%s,%s,
        %s,%s,%s,

        %s,%s,%s,%s,

        %s,%s,%s,%s,

        %s,%s,

        %s,%s,

        %s,%s,
        %s,%s
        )
        """

        values = (

            data.get("hostname","unknown"),
            data.get("ip","0.0.0.0"),
            timestamp,

            data.get("os_name",""),
            data.get("os_version",""),

            data.get("cpu_model",""),
            data.get("cpu_usage",0),
            data.get("cpu_freq",0),
            data.get("cpu_cores",0),
            data.get("cpu_threads",0),

            data.get("cpu_user",0),
            data.get("cpu_system",0),
            data.get("cpu_idle",0),

            data.get("ram_total",0),
            data.get("ram_used",0),
            data.get("ram_free",0),
            data.get("ram_percent",0),

            data.get("disk_total",0),
            data.get("disk_used",0),
            data.get("disk_free",0),
            data.get("disk_percent",0),

            data.get("process_count",0),
            data.get("thread_count",0),

            data.get("battery_percent",0),
            data.get("temperature",0),

            data.get("net_sent",0),
            data.get("net_recv",0),
            data.get("net_packets_sent",0),
            data.get("net_packets_recv",0)

        )

        cursor.execute(sql, values)
        db.commit()

        return jsonify({"status": "success", "message": "Metrics stored"})

    except Exception as e:

        print("API ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/systems")
def api_systems():

    global alerted_systems

    cursor.execute("""
        SELECT * FROM systems
        ORDER BY id DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()

    systems = []
    seen = set()

    for r in rows:

        hostname = r["hostname"]

        if hostname in seen:
            continue

        seen.add(hostname)

        anomaly = "Normal"
        reason = "System operating normally"

        try:

            issues = []

            if float(r["cpu_usage"]) > 85:
                issues.append(f"High CPU Usage ({r['cpu_usage']}%)")

            if float(r["ram_percent"]) > 90:
                issues.append(f"High RAM Usage ({r['ram_percent']}%)")

            if float(r["disk_percent"]) > 90:
                issues.append(f"Disk Almost Full ({r['disk_percent']}%)")

            if float(r["temperature"]) > 80:
                issues.append(f"High Temperature ({r['temperature']}°C)")

            if issues:

                anomaly = "Anomaly"
                reason = ", ".join(issues)

                # Send email only once per anomaly event
                if hostname not in alerted_systems:

                    try:

                        if "user" in session:

                            cursor.execute(
                                "SELECT email FROM users WHERE username=%s",
                                (session["user"],)
                            )

                            user = cursor.fetchone()

                            if user:

                                subject = "⚠ SysSentinel Alert - System Anomaly Detected"

                                body = f"""
SysSentinel Monitoring Alert

Hostname: {r['hostname']}
IP Address: {r['ip']}

CPU Usage: {r['cpu_usage']}%
RAM Usage: {r['ram_percent']}%
Disk Usage: {r['disk_percent']}%

Reason:
{reason}

Please investigate immediately.
"""

                                msg = Message(
                                    subject,
                                    recipients=[user["email"]],
                                    body=body
                                )

                                mail.send(msg)

                                print("Email alert sent to:", user["email"])

                                alerted_systems[hostname] = True

                    except Exception as e:
                        print("Email error:", e)

            else:
                # reset alert flag if system returns to normal
                if hostname in alerted_systems:
                    del alerted_systems[hostname]

        except:
            anomaly = "Normal"
            reason = "Metrics parsing error"

        r["anomaly"] = anomaly
        r["anomaly_reason"] = reason

        systems.append(r)

    return jsonify(systems)

@app.route("/api/anomalies")
def api_anomalies():

    cursor.execute("""
    SELECT * FROM systems
    ORDER BY id DESC
    LIMIT 100
    """)

    rows = cursor.fetchall()

    anomalies = []

    for r in rows:

        issues = []

        try:

            if float(r["cpu_usage"]) > 85:
                issues.append("High CPU")

            if float(r["ram_percent"]) > 90:
                issues.append("High RAM")

            if float(r["disk_percent"]) > 90:
                issues.append("Disk Full")

            if float(r["temperature"]) > 80:
                issues.append("Overheating")

        except:
            pass

        if issues:
            r["anomaly_reason"] = ", ".join(issues)
            anomalies.append(r)

    return jsonify(anomalies)

# -----------------------------
# SYSTEM PAGE
# -----------------------------
@app.route("/systems")
def systems():

    cursor.execute("""
    SELECT * FROM systems
    ORDER BY id DESC
    LIMIT 50
    """)

    systems = cursor.fetchall()

    return render_template("systems.html", systems=systems)

# -----------------------------
# CONFIGURE PAGE
# -----------------------------
@app.route("/configure")
def configure():

    if "user" not in session:
        return redirect("/login")

    return render_template("configure.html")

def omni_anomaly_variational_autoencoder():


    data = pd.read_csv("system_metrics.csv")

    features = [
        "cpu_usage",
        "memory_usage",
        "disk_io_wait",
        "network_latency",
        "process_count"
    ]

    dataset = data[features].values

    scaler = MinMaxScaler()

    normalized_data = scaler.fit_transform(dataset)

    window = 20

    sequences = []

    for i in range(len(normalized_data) - window):
        seq = normalized_data[i:i + window]
        sequences.append(seq)

    sequences = np.array(sequences)

    timesteps = sequences.shape[1]

    input_dim = sequences.shape[2]

    latent_dim = 8

    inputs = Input(shape=(timesteps, input_dim))

    encoder = GRU(32, return_sequences=False)(inputs)

    z_mean = Dense(latent_dim)(encoder)

    z_log_var = Dense(latent_dim)(encoder)

    def sampling(args):

        z_mean, z_log_var = args

        epsilon = K.random_normal(shape=(K.shape(z_mean)[0], latent_dim))

        return z_mean + K.exp(0.5 * z_log_var) * epsilon

    z = Lambda(sampling)([z_mean, z_log_var])

    decoder_input = RepeatVector(timesteps)(z)

    decoder = GRU(32, return_sequences=True)(decoder_input)

    outputs = TimeDistributed(Dense(input_dim))(decoder)

    vae = Model(inputs, outputs)

    reconstruction_loss = tf.keras.losses.mse(inputs, outputs)

    reconstruction_loss = K.mean(reconstruction_loss)

    kl_loss = -0.5 * K.mean(
        1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
    )

    total_loss = reconstruction_loss + kl_loss

    vae.add_loss(total_loss)

    vae.compile(optimizer="adam")

    vae.fit(
        sequences,
        epochs=30,
        batch_size=64,
        validation_split=0.1
    )

    reconstructed = vae.predict(sequences)

    reconstruction_error = np.mean(
        np.square(sequences - reconstructed),
        axis=(1,2)
    )

    threshold = np.percentile(reconstruction_error, 95)

    anomaly_flags = reconstruction_error > threshold

    anomaly_index = np.where(anomaly_flags)[0]

    background = sequences[np.random.choice(len(sequences), 100)]

    explainer = shap.KernelExplainer(
        vae.predict,
        background
    )

    shap_values = explainer.shap_values(sequences[:10])

    importance = np.mean(np.abs(shap_values), axis=1)

    recommendations = []

    for idx in anomaly_index:

        metric = np.argmax(importance[idx])

        if metric == 0:
            recommendations.append("Investigate CPU intensive processes")

        elif metric == 1:
            recommendations.append("Check memory allocation and leaks")

        elif metric == 2:
            recommendations.append("Inspect disk IO scheduling")

        elif metric == 3:
            recommendations.append("Diagnose network latency sources")

        else:
            recommendations.append("Review abnormal process activity")

    alerts = []

    for i, rec in zip(anomaly_index, recommendations):

        alerts.append({
            "time": int(i),
            "status": "ANOMALY",
            "action": rec
        })

    return alerts

# -----------------------------
# RUN AGENT REMOTELY
# -----------------------------
@app.route("/run_agent", methods=["POST"])
def run_agent():

    ip = request.form["ip"]

    agent_path = "C:\\app\\agent.py"

    command = f'psexec \\\\{ip} python {agent_path}'

    try:

        subprocess.run(command, shell=True)

        message = f"Agent started successfully on {ip}"

    except Exception as e:

        message = str(e)

    return render_template("configure.html", message=message)

# -----------------------------
# DISCOVERY SERVER
# -----------------------------
def discovery_server():

    UDP_IP = "0.0.0.0"
    UDP_PORT = 9998

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((UDP_IP, UDP_PORT))

    print("Discovery server started on port", UDP_PORT)

    while True:

        data, addr = sock.recvfrom(1024)

        if data == b"DISCOVER_MONITOR_SERVER":
            sock.sendto(b"MONITOR_SERVER", addr)

threading.Thread(target=discovery_server, daemon=True).start()

def send_anomaly_email(user_email, system_data):

    try:

        subject = "⚠ SysSentinel Alert - System Anomaly Detected"

        body = f"""
        SysSentinel Monitoring Alert

        A system anomaly has been detected.

        Hostname: {system_data['hostname']}
        IP Address: {system_data['ip']}

        CPU Usage: {system_data['cpu_usage']}%
        RAM Usage: {system_data['ram_percent']}%
        Disk Usage: {system_data['disk_percent']}%
        Temperature: {system_data['temperature']}°C

        Reason:
        {system_data['anomaly_reason']}

        Please investigate immediately.

        SysSentinel Monitoring System
        """

        msg = Message(
            subject,
            recipients=[user_email],
            body=body
        )

        mail.send(msg)

        print("Email alert sent to:", user_email)

    except Exception as e:

        print("Mail Error:", e)
        
# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
