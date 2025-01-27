# Saé503 - Orchestrer la conteneurisation d’une application 
Elaboré par **Loris Egault** & **Simon Rageul** ***(Binôme 5)***
#### Promotion BUT3 FA *2024-2025*
---
# Lot 2 : Cahier d'installation technique (CIT)

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