import streamlit as st
import pandas as pd
import time
import sqlite3
import requests

# URL de votre API Flask
API_URL = 'http://localhost:5000/api/donnees'

# Nom de la base de données SQLite
DB_NAME = "dashboard_data.db"

# Fonction pour initialiser la base SQLite
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Création de la table si elle n'existe pas encore
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS donnees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            type TEXT NOT NULL,
            value INTEGER NOT NULL  
        )
        """)
        conn.commit()

# Fonction pour insérer les données dans la base SQLite
def insert_data_to_db(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Insertion des données
        for row in data:
            cursor.execute("""
            INSERT INTO donnees (timestamp, type, value)
            VALUES (?, ?, ?)
            """, (row['timestamp'], row['type'], row['value']))
        conn.commit()

# Fonction pour charger les données depuis l'API
def load_data_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur lors de la récupération des données : {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Erreur lors de la connexion à l'API : {e}")
        return []

# Fonction pour récupérer les données depuis SQLite
def load_data_from_db():
    with sqlite3.connect(DB_NAME) as conn:
        query = "SELECT timestamp, type, value FROM donnees ORDER BY timestamp"
        return pd.read_sql_query(query, conn)

# Initialisation de la base de données
init_db()

# Conteneur pour l'affichage dynamique
placeholder = st.empty()

# Configuration de la fréquence de mise à jour
update_frequency = st.slider("Fréquence de mise à jour (secondes)", 1, 10, 1)

# Boucle pour mettre à jour le dashboard
while True:
    # Charger les données depuis l'API et les insérer dans la base SQLite
    api_data = load_data_from_api()
    if api_data:
        insert_data_to_db(api_data)  # Insertion des données de l'API dans SQLite

    # Charger les données depuis SQLite
    df = load_data_from_db()
    if not df.empty:
        # Conversion en datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # Calcul de l'occupation en temps réel
        df['occupation_change'] = df['type'].map({'entree': 1, 'sortie': -1}) * df['value']
        df['occupation'] = df['occupation_change'].cumsum()

        # Calcul des métriques
        total_entries = df[df['type'] == 'entree']['value'].sum()
        total_exits = df[df['type'] == 'sortie']['value'].sum()
        current_in_building = df['occupation'].iloc[-1]

        # Mettre à jour le dashboard
        with placeholder.container():
            # Affichage des métriques
            st.subheader("Statistiques en temps réel :")
            col1, col2, col3 = st.columns(3)
            col1.metric("Personnes dans le bâtiment", int(current_in_building),help="Personnes dans le bâtiment actuellement", label_visibility="visible")

            col2.metric("Total entrées", int(total_entries),help="Total d'entrées depuis le début de la journée", label_visibility="visible")

            col3.metric("Total sorties", int(total_exits),help="Total de sorties depuis le début de la journée", label_visibility="visible")

            # Affichage des dernières données (ex. 20 dernières lignes)
            st.subheader("Dernières données :")
            st.write(df.tail(20))

            # Affichage d'un graphique dynamique de l'occupation
            st.subheader("Occupation en temps réel :")
            st.line_chart(df.set_index("timestamp")["occupation"], color = "#24b2a6", width=1000,use_container_width=False)

    else:
        with placeholder.container():
            st.subheader("Aucune donnée disponible")
            st.write("En attente de données...")

    # Pause avant la prochaine mise à jour
    time.sleep(update_frequency)
