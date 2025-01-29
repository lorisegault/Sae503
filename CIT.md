# Saé503 - Orchestrer la conteneurisation d’une application 
Elaboré par **Loris Egault** & **Simon Rageul** ***(Binôme 5)***
#### Promotion BUT3 FA *2024-2025*
---
# Lot 2 : Cahier d'installation technique (CIT)

### Niveau Matériel

Nous utilisons une machine Linux avec Minikube hébergé sur le Proxmox IUT. 

Celle ci présente les caractéristiques suivantes : 

- RAM : 4 Gb
- Processeur : 2 sockets, 1 core
- Stockage : 12 Gb
- OS : Debian12 + Minikube
- @IP : 172.18.53.105 / 16
- GW : 172.18.0.254
- DNS : 172.19.11.252 , 129.20.211.23

### Niveau logiciel

#### Installation de Docker

Nous installons Docker sur la machine linux avec les commandes suivantes : 
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
Nous installons les paquets Docker : 
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Puis nous pouvons tester le focntionnement de Docker en créeant un conteneur utilisant l'image `hello-world`: 
```bash
sudo docker run hello-world
```

#### Installation de Minikube

Dans notre cas Minikube est déjà installé sur la VM Linux mais pour installer Minikube on peut suivre les consignes du site suivant : 

<a href="https://kubernetes.io/fr/docs/tasks/tools/install-minikube/">
https://kubernetes.io/fr/docs/tasks/tools/install-minikube/
</a>

On peut ensuite installer `kubectl` en utilisant les consignes du site suivant : 

<a href="https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux">
https://kubernetes.io/fr/docs/tasks/tools/install-kubectl/#install-kubectl-on-linux
</a>

#### Installation de sudo et gestion des droits

Pour une question de praticité on installe `sudo` sur la machine Linux : 
```bash
root@Minikube:/home/user# apt install sudo
```

On peut ensuite ajouter l'utilisateur `sudo` dans le fichier `/etc/sudoers` pour règler ses droits sur la machine. 

On ajoute également l'utilisateur actuel au groupe Docker et on applique les changements immédiatement :
```bash
sudo usermod -aG docker $USER && newgrp docker
```

#### Utilisation de Minikube

On peut ensuite démarrer minikube : 
```bash
user@Minikube:~$ minikube start --driver=docker
😄  minikube v1.35.0 sur Debian 12.9 (kvm/amd64)
✨  Choix automatique du pilote docker
📌  Utilisation du pilote Docker avec le privilège root
👍  Démarrage du nœud "minikube" primary control-plane dans le cluster "minikube"
🚜  Extraction de l'image de base v0.0.46...
💾  Téléchargement du préchargement de Kubernetes v1.32.0...
	> preloaded-images-k8s-v18-v1...:  333.57 MiB / 333.57 MiB  100.00% 26.24 M
	> gcr.io/k8s-minikube/kicbase...:  500.31 MiB / 500.31 MiB  100.00% 25.85 M

🔥  Création de docker container (CPU=2, Memory=2200Mo) ...
🐳  Préparation de Kubernetes v1.32.0 sur Docker 27.4.1...
	▪ Génération des certificats et des clés
	▪ Démarrage du plan de contrôle ...
	▪ Configuration des règles RBAC ...
🔗  Configuration de bridge CNI (Container Networking Interface)...
🔎  Vérification des composants Kubernetes...
	▪ Utilisation de l'image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Modules activés: storage-provisioner, default-storageclass
🏄  Terminé ! kubectl est maintenant configuré pour utiliser "minikube" c
```
On peut alors utiliser Minikube comme orchestrateur !

Nous avons ensuite crée 2 namespace permettant de distinguer les environnements  `qualification` et `production`: 
```bash
user@Minikube:~$ kubectl create namespace qualification
namespace/qualification created

user@Minikube:~$ kubectl create namespace production
namespace/production created
```
