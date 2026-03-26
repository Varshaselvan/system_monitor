import psutil
import platform
import socket
import requests
import time
import datetime


# -----------------------------
# SERVER DISCOVERY
# -----------------------------

def discover_server():

    BROADCAST_PORT = 9998
    MESSAGE = b"DISCOVER_MONITOR_SERVER"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(3)

    try:

        s.sendto(MESSAGE, ('255.255.255.255', BROADCAST_PORT))

        data, addr = s.recvfrom(1024)

        print("Server discovered:", addr[0])

        return f"http://{addr[0]}:5000/api/metrics"

    except:

        return None


# -----------------------------
# FALLBACK SERVER
# -----------------------------

SERVER = discover_server()

if not SERVER:
    SERVER = "https://dd7b-2405-201-e038-50d7-7db6-2ce4-6c8e-cc1d.ngrok-free.app/api/metrics"
    print("Using fallback server:", SERVER)


# -----------------------------
# UTILS
# -----------------------------

def bytes_to_gb(value):
    return round(value / (1024**3), 2)


# -----------------------------
# COLLECT METRICS
# -----------------------------

def get_metrics():

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os_name = platform.system()
    os_version = platform.release()

    cpu_model = platform.processor()

    cpu_usage = psutil.cpu_percent(interval=1)

    cpu_times = psutil.cpu_times_percent()

    cpu_user = cpu_times.user
    cpu_system = cpu_times.system
    cpu_idle = cpu_times.idle

    freq = psutil.cpu_freq()
    cpu_freq = freq.current if freq else 0

    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()

    ram_total = bytes_to_gb(mem.total)
    ram_used = bytes_to_gb(mem.used)
    ram_free = bytes_to_gb(mem.available)
    ram_percent = mem.percent

    disk = psutil.disk_usage('/')

    disk_total = bytes_to_gb(disk.total)
    disk_used = bytes_to_gb(disk.used)
    disk_free = bytes_to_gb(disk.free)
    disk_percent = disk.percent

    net = psutil.net_io_counters()

    process_count = len(psutil.pids())

    thread_count = sum(p.num_threads() for p in psutil.process_iter())

    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else 100

    temperature = 0

    try:
        temps = psutil.sensors_temperatures()
        if temps:
            temperature = list(temps.values())[0][0].current
    except:
        pass

    data = {

        "hostname": hostname,
        "ip": ip,
        "timestamp": timestamp,

        "os_name": os_name,
        "os_version": os_version,

        "cpu_model": cpu_model,
        "cpu_usage": cpu_usage,
        "cpu_freq": cpu_freq,
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,

        "cpu_user": cpu_user,
        "cpu_system": cpu_system,
        "cpu_idle": cpu_idle,

        "ram_total": ram_total,
        "ram_used": ram_used,
        "ram_free": ram_free,
        "ram_percent": ram_percent,

        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_free": disk_free,
        "disk_percent": disk_percent,

        "process_count": process_count,
        "thread_count": thread_count,

        "battery_percent": battery_percent,
        "temperature": temperature,

        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
        "net_packets_sent": net.packets_sent,
        "net_packets_recv": net.packets_recv

    }

    return data


# -----------------------------
# MAIN LOOP
# -----------------------------

print("Monitoring agent started...")

while True:

    try:

        metrics = get_metrics()

        response = requests.post(SERVER, json=metrics, timeout=5)

        print(
            f"[{metrics['timestamp']}] Sent metrics from {metrics['hostname']} | CPU {metrics['cpu_usage']}%"
        )

    except Exception as e:

        print("Connection error:", e)

    time.sleep(5)
