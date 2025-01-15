import os
import requests
from django.shortcuts import render
from .forms import SparqlQueryForm
import json
from rdflib import Graph , URIRef
from django.http import JsonResponse
# URL de votre serveur Fuseki et de votre dataset
FUSEKI_URL = "http://localhost:3030/my_ontology/sparql"  # Remplacez par l'URL correcte de votre serveur Fuseki

def query_sparql(request):
    response_data = None
    sparql_results = None
    graph_data = {"nodes": [], "edges": []}

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

            if response.status_code == 200:
                try:
                    sparql_results = response.json()

                except ValueError:
                    sparql_results = {"error": "La réponse du serveur n'est pas au format JSON."}
            else:
                sparql_results = {"error": f"Erreur {response.status_code}: {response.text}"}
    else:
        form = SparqlQueryForm()

    return render(request, 'sparql_query/query.html', {
        'form': form,
        'sparql_results': sparql_results,
        'graph_data': graph_data
    })



def afficher_graphe(request):
    return render(request, 'sparql_query/visualiser_graphe.html')


def get_graph_data(request):
    # Définir le chemin complet vers le fichier ontology.ttl
    ontology_path = os.path.join("C:/Users/USER/Desktop/ontology/Projet-SPARQL", "ontology.ttl")

    # Charger le fichier RDF en format Turtle
    graph = Graph()
    graph.parse(ontology_path, format="ttl")  # Utiliser parse() avec le bon chemin

    # Extraire les classes et les propriétés du graphe RDF
    nodes = []
    edges = []

    for s, p, o in graph:
        if isinstance(s, URIRef):
            nodes.append({"id": str(s), "label": str(s)})
        if isinstance(o, URIRef):
            nodes.append({"id": str(o), "label": str(o)})

        edges.append({"source": str(s), "target": str(o), "label": str(p)})

    unique_nodes = {node["id"]: node for node in nodes}.values()

    # Filtrer les arêtes pour ne conserver que celles qui référencent des nœuds valides
    valid_ids = {node["id"] for node in unique_nodes}
    valid_edges = [edge for edge in edges if edge["source"] in valid_ids and edge["target"] in valid_ids]

    return JsonResponse({"nodes": list(unique_nodes), "edges": valid_edges})