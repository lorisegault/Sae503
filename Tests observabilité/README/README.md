# Tableau de Bord avec Grafana et Prometheus

Ce projet implémente un tableau de bord pour surveiller l'utilisation des ressources système et les performances d'une base de données Redis. Il intègre **Prometheus** pour la collecte des métriques et **Grafana** pour la visualisation des données.

## 📌 Fonctionnalités
- Surveillance des **ressources système** (CPU, mémoire, conteneurs Docker).
- Mesure du **temps de réponse de Redis**.
- **Alertes par e-mail** en cas de dépassement de seuils critiques.
- **Exposition des métriques** sur un endpoint compatible Prometheus (`/metrics`).
- **Affichage d'un tableau de bord** JSON (`/dashboard`).

---

## 📦 Installation et Configuration

### 1️⃣ Prérequis
- **Python 3.x**
- **Prometheus** et **Grafana** installés
- **Redis** en cours d'exécution

### 2️⃣ Installation des dépendances
```sh
pip install flask psutil docker redis prometheus_client
```

### 3️⃣ Lancer l'application
```sh
python dashboard_grafana.py
```
Cela démarre :
- Un serveur Flask exposant les métriques sur `http://localhost:5000/metrics`
- Un serveur Prometheus sur `http://localhost:8000`

---

## 🔧 Configuration de Prometheus

Créer un fichier `prometheus.yml` :
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['localhost:8000']
```

Puis lancer **Prometheus** :
```sh
prometheus --config.file=prometheus.yml
```

---

## 📊 Configuration de Grafana
1. **Ajout de Prometheus comme source de données**
   - Aller dans **Grafana > Configuration > Data Sources**
   - Ajouter **Prometheus** avec l’URL : `http://localhost:9090`

---

## 🛠️ Dépannage
- Vérifier que **Redis fonctionne** avec `redis-cli ping`
- S'assurer que **Prometheus collecte les métriques** (`http://localhost:9090/targets`)
- Consulter les logs de Grafana pour vérifier la connexion à Prometheus

