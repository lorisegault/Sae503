import time
import psutil
import docker
from flask import Flask, request, jsonify
from redis import Redis
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from prometheus_client import Gauge, Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server

app = Flask(__name__)
redis_client = Redis(host='localhost', port=6379, db=0)

# Déclaration des métriques Prometheus
db_response_time_gauge = Gauge('db_response_time', 'Temps de réponse de Redis')
cpu_usage_gauge = Gauge('cpu_usage', 'Utilisation du CPU en pourcentage')
memory_usage_gauge = Gauge('memory_usage', 'Utilisation de la mémoire en pourcentage')
request_count = Counter('request_count', 'Nombre total de requêtes', ['endpoint'])
running_containers_gauge = Gauge('running_containers', 'Nombre de containers en cours d\'exécution')

# Fonction pour mesurer le temps de réponse de Redis
def measure_db_response_time():
    start_time = time.time()
    redis_client.ping()
    end_time = time.time()
    response_time = end_time - start_time
    db_response_time_gauge.set(response_time)
    return response_time

# Middleware pour compter les requêtes
@app.before_request
def count_requests():
    endpoint = request.endpoint
    request_count.labels(endpoint).inc()

# Fonction pour surveiller les ressources système
def monitor_resources():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        db_response_time = measure_db_response_time()

        cpu_usage_gauge.set(cpu_usage)
        memory_usage_gauge.set(memory_usage)
        db_response_time_gauge.set(db_response_time)

        docker_client = docker.from_env()
        running_containers_gauge.set(len(docker_client.containers.list()))

        time.sleep(5)

# Fonction pour envoyer une alerte par email
def send_alert(subject, message):
    sender_email = "your_email@example.com"
    receiver_email = "alert_receiver@example.com"
    password = "your_password"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Vérification des alertes
def check_alerts():
    while True:
        if db_response_time_gauge._value.get() > 1:
            send_alert("Alerte : Temps de réponse élevé", "Le temps de réponse de la base de données dépasse 1 seconde.")
        if cpu_usage_gauge._value.get() > 80:
            send_alert("Alerte : Utilisation élevée du CPU", "L'utilisation du CPU dépasse 80%.")
        if memory_usage_gauge._value.get() > 80:
            send_alert("Alerte : Utilisation élevée de la mémoire", "L'utilisation de la mémoire dépasse 80%.")
        time.sleep(300)

# Endpoint pour afficher le tableau de bord
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        "db_response_time": db_response_time_gauge._value.get(),
        "cpu_usage": cpu_usage_gauge._value.get(),
        "memory_usage": memory_usage_gauge._value.get(),
        "running_containers": running_containers_gauge._value.get()
    }), 200

# Exposition des métriques Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Lancer les threads pour la surveillance
if __name__ == '__main__':
    start_http_server(8000)  # Expose les métriques sur le port 8000
    Thread(target=monitor_resources, daemon=True).start()
    Thread(target=check_alerts, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
