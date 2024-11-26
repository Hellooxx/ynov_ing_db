from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
CORS(app)
api = Api(app)

# Données en mémoire pour l'exemple
donnees = []

class DonneesList(Resource):
    def get(self):
        return donnees, 200

    def post(self):
        if request.is_json:
            contenu = request.get_json()
            # Ajouter un horodatage serveur si nécessaire
            contenu['reception_timestamp'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            donnees.append(contenu)
            return {'message': 'Données reçues avec succès'}, 201
        else:
            return {'message': 'Format de données invalide'}, 400

@app.route('/')
def hello_world():
    return 'Hello, World!'
# Ajout de la ressource à l'API
api.add_resource(DonneesList, '/api/donnees')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
