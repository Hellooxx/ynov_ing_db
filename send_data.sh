#!/bin/bash

# Adresse de votre API
API_URL="http://localhost:5000/api/donnees"

# Horodatage de départ
start_time="2024-11-25 08:00:00"

# Nombre d'enregistrements à envoyer
num_records=50

# Intervalle entre les horodatages (en minutes)
interval_minutes=5

# Convertir start_time en timestamp UNIX
start_timestamp=$(date -j -f "%Y-%m-%d %H:%M:%S" "$start_time" "+%s")

# Boucle pour envoyer les données
for ((i=0; i<$num_records; i++))
do
  # Calculer le timestamp UNIX actuel
  current_timestamp=$((start_timestamp + (i * interval_minutes * 60)))

  # Convertir le timestamp UNIX en horodatage formaté
  current_time=$(date -j -f "%s" "$current_timestamp" +"%Y-%m-%d %H:%M:%S")
  
  # Générer une valeur aléatoire pour 'value'
  value=$(( (RANDOM % 20) + 1 ))

  # Déterminer aléatoirement si c'est une entrée ou une sortie
  if (( RANDOM % 2 == 0 )); then
    type="entree"
  else
    type="sortie"
  fi

  # Construire les données JSON
  json_data=$(printf '{"timestamp": "%s", "value": %d, "type": "%s"}' "$current_time" "$value" "$type")

  # Afficher les données envoyées
  echo "Envoi des données : $json_data"

  # Envoyer la requête POST à l'API
  curl -X POST -H "Content-Type: application/json" -d "$json_data" $API_URL

  # Pause d'une seconde entre les requêtes (optionnel)
  sleep 1
done
