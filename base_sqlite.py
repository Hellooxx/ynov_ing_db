import sqlite3
import json

# Charger les données depuis le fichier JSON
with open('data_example.json', 'r') as file:
    data = json.load(file)

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Création de la table (si elle n'existe pas déjà)
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    value INTEGER NOT NULL
)
''')

# Insérer les données dans la table
for entry in data:
    cursor.execute('INSERT INTO data (timestamp, value) VALUES (?, ?)', (entry['timestamp'], entry['value']))

# Sauvegarder et fermer la connexion
conn.commit()
conn.close()
