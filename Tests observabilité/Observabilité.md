# Explications du fichier Tableau_de_bord_mecanisme_alerte.py :

## Temps de réponse de la base de données :
  La fonction measure_db_response_time mesure le temps de réponse de Redis et l'ajoute aux métriques.

## Évolution du nombre de requêtes :
  Le middleware count_requests incrémente un compteur pour chaque endpoint.

## Nombre de conteneurs en cours d'exécution :
  La bibliothèque Docker SDK est utilisée pour compter les conteneurs en cours d'exécution.

## Mémoire et CPU utilisés :
  La bibliothèque psutil est utilisée pour surveiller l'utilisation des ressources.

## Mécanisme d'alerte :
  La fonction send_alert envoie un email en cas de dépassement des seuils définis.

## Tableau de bord :
  L'endpoint /dashboard retourne les métriques sous forme de JSON.

## *Prérequis* :

Installer les bibliothèques nécessaires : **pip install psutil docker**.
Configurer un compte email pour l'envoi des alertes :
**modifier**
    sender_email = "your_email@example.com"
    receiver_email = "alert_receiver@example.com"
    password = "your_password"
