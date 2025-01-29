import time
import psutil
import docker
from flask import Flask, request, jsonify
from redis import Redis
from threading import Thread
import smtplib
from email.mime.text import MIMEText

# Ajout de métriques
metrics = {
    "db_response_time": [],
    "request_count": {},
    "cpu_usage": [],
    "memory_usage": [],
    "running_containers": 0
}

# Fonction pour mesurer le temps de réponse de Redis
def measure_db_response_time():
    start_time = time.time()
    redis_client.ping()
    end_time = time.time()
    response_time = end_time - start_time
    metrics["db_response_time"].append(response_time)

# Middleware pour compter les requêtes
@app.before_request
def count_requests():
    endpoint = request.endpoint
    if endpoint not in metrics["request_count"]:
        metrics["request_count"][endpoint] = 0
    metrics["request_count"][endpoint] += 1

# Fonction pour surveiller les ressources système
def monitor_resources():
    while True:
        metrics["cpu_usage"].append(psutil.cpu_percent(interval=1))
        metrics["memory_usage"].append(psutil.virtual_memory().percent)
        docker_client = docker.from_env()
        metrics["running_containers"] = len(docker_client.containers.list())
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
        if len(metrics["db_response_time"]) > 0 and max(metrics["db_response_time"]) > 1:
            send_alert("Alerte : Temps de réponse élevé", "Le temps de réponse de la base de données dépasse 1 seconde.")
        if len(metrics["cpu_usage"]) > 0 and max(metrics["cpu_usage"]) > 80:
            send_alert("Alerte : Utilisation élevée du CPU", "L'utilisation du CPU dépasse 80%.")
        if len(metrics["memory_usage"]) > 0 and max(metrics["memory_usage"]) > 80:
            send_alert("Alerte : Utilisation élevée de la mémoire", "L'utilisation de la mémoire dépasse 80%.")
        time.sleep(300)

# Endpoint pour afficher le tableau de bord
@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Tableau de bord synthétique
    ---
    responses:
      200:
        description: Données du tableau de bord
    """
    return jsonify(metrics), 200

# Lancer les threads pour la surveillance
if __name__ == '__main__':
    Thread(target=monitor_resources, daemon=True).start()
    Thread(target=check_alerts, daemon=True).start()
    app.run(host='0.0.0.0', port=APP_PORT)
