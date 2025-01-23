# Saé503 - Orchestrer la conteneurisation d’une application 
Elaboré par **Loris Egault** & **Simon Rageul** ***(Binôme 5)***
##### 📅 23 janvier 2025
#### Promotion BUT3 FA *2024-2025*
---
## Lot 1 : Définition de l'architecture
![Diagramme de l'architecture technique](SchémaSAE503.svg)
## Lot 2 : Mise en place et configuration d'un orchestrateur de conteneurs

### Liens utilisés

##### Installation de docker :
<a href="https://docs.docker.com/engine/install/debian/">
  <img src="imgs/docker.webp" width="50">
</a>
https://docs.docker.com/engine/install/debian/

##### Installation de minikube :
<a href="https://kubernetes.io/fr/docs/tasks/tools/install-minikube/">
  <img src="imgs/minikube.png" width="50">
</a>
https://kubernetes.io/fr/docs/tasks/tools/install-minikube/

##### Installation de kubectl :
<a href="https://kubernetes.io/fr/docs/tasks/tools/install-minikube/">
  <img src="imgs/kubectl.svg" width="50">
</a>
https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux

### Commandes bash
Ajoute l'utilisateur actuel au groupe Docker et applique les changements immédiatement :
```bash
sudo usermod -aG docker $USER && newgrp docker
```
Commande pour se mettre en **root (avec minikube)**
```bash
root@Minikube:/home/user# apt install sudo
```
Démarrer minikube
```bash
@Minikube:~$ minikube start
```
##### Création de 2 namespaces correspondant aux 2 plateformes qualification et production : 
```bash
user@Minikube:~$ kubectl create namespace qualification
namespace/qualification created

user@Minikube:~$ kubectl create namespace production
namespace/production created
```
## Lot 3 : Refactorisation de l’application
#### Installation de python sur la VM pour tester indépendamment nos api (et installer les modules : flask, redis, swagger *et* wraps)
## *Objectifs*
- Découper l'application monolithique en trois microservices distincts pour chaque fonctionnalité principale : /users, /quotes, et /search.
- Respecter les bonnes pratiques en matière de conteneurisation, telles que l'utilisation d'images Docker minimales et la variabilisation des paramètres.
- Assurer la compatibilité avec l'orchestrateur pour un déploiement simplifié et performant.
### Étapes de refactorisation
#### Découpage en trois microservices

Le code Python fourni a été adapté pour être divisé en trois fichiers distincts correspondant aux points d'accès :

- /users : gestion des utilisateurs (ajout, récupération).
- /quotes : gestion des citations (ajout, suppression, récupération).
- /search : recherche de citations par mot-clé.

Chaque microservice a son propre fichier Flask et fonctionne indépendamment.
### Création des Dockerfiles

Chaque microservice dispose d'un fichier Dockerfile optimisé :

#### Exemple de Dockerfile pour /users :

##### Utiliser une image Python minimale
```python
FROM python:3.10-slim
```
##### Définir le répertoire de travail
```bash
WORKDIR /app
```
##### Copier les fichiers nécessaires
```bash
COPY requirements.txt .
COPY users_service.py .
```
##### Installer les dépendances
```python
RUN pip install --no-cache-dir -r requirements.txt
```
##### Exposer le port
```bash   
EXPOSE 5000
```
##### Lancer l'application (dockerfile)
```Dockerfile
CMD ["python", "users_service.py"]
```
##### Commandes pour construire et publier l'image Docker :
```bash
docker build -t loris-egault/users-service:latest .
docker push loris-egault/users-service:latest
```
#### Variabilisation des paramètres

Les paramètres sensibles (comme les mots de passe et les URL des bases de données) sont externalisés sous forme de variables d'environnement pour améliorer la sécurité et la portabilité :

##### Exemple dans le code Python :
```python
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
ADMIN_KEY = os.getenv("ADMIN_KEY", "default_key")
```
##### Exemple de fichier .env pour chaque environnement (qualification et production) :
```python
REDIS_HOST=redis-qualification
REDIS_PORT=6379
ADMIN_KEY=supersecretkey
```
#### Tests des microservices

*Chaque microservice est testé indépendamment sur une machine virtuelle avant le déploiement* :

##### Installation des modules nécessaires :
```python
pip install flask redis flasgger wraps
```
##### Commande pour tester un microservice (/users) en local :
```python
python users_service.py
```
##### Exemple de requête pour tester l'API /users :
```bash
curl -X POST http://localhost:5000/users -H "Authorization: supersecretkey" -d '{"id": "1", "name": "Tintin", "password": "milou"}'
curl -X GET http://localhost:5000/users -H "Authorization: supersecretkey"
```
## Lot 4 : Instanciation de l'application dans l'orchestrateur
## *Objectifs*

- Déployer les microservices dans des conteneurs sur deux plateformes cloisonnées : qualification et production.
- Configurer un orchestrateur de conteneurs (Kubernetes via Minikube) pour assurer la montée en charge et la haute disponibilité.
- Intégrer un reverse proxy pour gérer les requêtes entrantes et limiter les ressources allouées entre les plateformes.

### Étapes de déploiement

#### Création des déploiements et services Kubernetes

Chaque microservice est associé à un déploiement et un service exposé dans Kubernetes :

##### Déploiement pour le service /users :
```python
apiVersion: apps/v1
kind: Deployment
metadata:
  name: users-deployment
  namespace: qualification
spec:
  replicas: 2
  selector:
    matchLabels:
      app: users
  template:
    metadata:
      labels:
        app: users
    spec:
      containers:
      - name: users
        image: loris-egault/users-service:latest
        ports:
        - containerPort: 5000
```
##### Déploiement pour le service /quotes :
```python
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quotes-deployment
  namespace: qualification
spec:
  replicas: 2
  selector:
    matchLabels:
      app: quotes
  template:
    metadata:
      labels:
        app: quotes
    spec:
      containers:
      - name: quotes
        image: loris-egault/quotes-service:latest
        ports:
        - containerPort: 5000
```
##### Déploiement pour le service /search :
```python
apiVersion: apps/v1
kind: Deployment
metadata:
  name: search-deployment
  namespace: qualification
spec:
  replicas: 2
  selector:
    matchLabels:
      app: search
  template:
    metadata:
      labels:
        app: search
    spec:
      containers:
      - name: search
        image: loris-egault/search-service:latest
        ports:
        - containerPort: 5000
```
### Configuration du reverse proxy avec Traefik

Un fichier de configuration YAML doit être créé pour intégrer Traefik en tant que proxy inversé :

##### Exemple de fichier traefik-ingress.yaml :
```python
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: traefik-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: traefik
spec:
  rules:
  - host: qualification-app.nip.io
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: users-service
            port:
              number: 5000
      - path: /quotes
        pathType: Prefix
        backend:
          service:
            name: quotes-service
            port:
              number: 5000
```
### Gestion des ressources
```python
Allocation de quotas de CPU et de mémoire pour les namespaces :

apiVersion: v1
kind: ResourceQuota
metadata:
  name: resource-quota
  namespace: production
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
```
### Configuration des limites de requêtes

Traefik a été configuré pour limiter les requêtes HTTP à 10 par minute afin de protéger les ressources.
## Lot 5 : Mise en place d'une couche d'observabilité
## *Objectifs*

- Fournir un tableau de bord détaillé pour surveiller les performances de l'application et des plateformes.
- Mettre en place un mécanisme d'alerte en cas de surcharge ou d'erreurs critiques.

### Outils utilisés

- Prometheus : pour collecter les métriques système et applicatives.
- Grafana : pour visualiser les métriques dans des tableaux de bord.
- AlertManager : pour configurer des alertes.

### Étapes de mise en place
#### Déploiement de Prometheus

##### Exemple de fichier prometheus-deployment.yaml :
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-deployment
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
```
#### Configuration de Grafana

##### Tableau de bord contenant :
- Le temps de réponse des API.
- Le nombre de conteneurs en exécution.
- La mémoire et CPU utilisés.
- Le nombre de requêtes par service.

### Mécanisme d'alerte

#### Configuration d'AlertManager pour envoyer des alertes via email en cas de :

- Taux élevé de requêtes échouées.
- Surcharge CPU ou mémoire dépassant un seuil défini.
