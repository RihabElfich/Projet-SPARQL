import requests
from django.shortcuts import render
from .forms import SparqlQueryForm
import json

# URL de votre serveur Fuseki et de votre dataset
FUSEKI_URL = "http://localhost:3030/my_ontology/sparql"  # Remplacez par l'URL correcte de votre serveur Fuseki

def query_sparql(request):
    response_data = None

    if request.method == 'POST':
        form = SparqlQueryForm(request.POST)

        if form.is_valid():
            sparql_query = form.cleaned_data['sparql_query']

            # Paramètres pour envoyer la requête à Fuseki
            params = {
                'query': sparql_query,
                'format': 'application/sparql-results+json'
            }

            # Envoi de la requête à Fuseki
            response = requests.get(FUSEKI_URL, params=params)

            # Vérification de la réponse
            if response.status_code == 200:
                try:
                    # Tenter de décoder la réponse JSON
                    response_data = response.json()
                except ValueError:
                    # Si la réponse n'est pas un JSON valide, afficher le texte brut
                    response_data = {"error": "La réponse du serveur n'est pas au format JSON."}
            else:
                response_data = {"error": f"Erreur {response.status_code}: {response.text}"}
    else:
        form = SparqlQueryForm()

    # Retourner le résultat à la vue
    return render(request, 'sparql_query/query.html', {'form': form, 'response_data': response_data})
