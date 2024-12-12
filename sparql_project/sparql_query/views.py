from django.shortcuts import render
import requests
from .forms import SparqlQueryForm

def query_sparql(request):
    response_data = None
    if request.method == 'POST':
        form = SparqlQueryForm(request.POST)
        if form.is_valid():
            sparql_query = form.cleaned_data['sparql_query']

            # URL de l'API DBpedia SPARQL
            endpoint_url = "https://dbpedia.org/sparql"

            # Faire la requête
            response = requests.get(endpoint_url, params={'query': sparql_query, 'format': 'application/sparql-results+json'})

            # Vérifier la réponse
            if response.status_code == 200:
                response_data = response.json()

                # Extract relevant data from the response (generic extraction)
                if 'results' in response_data and 'bindings' in response_data['results']:
                    results = []
                    for binding in response_data['results']['bindings']:
                        result_info = {}
                        # Iterate over each key-value pair in the binding
                        for key, value in binding.items():
                            result_info[key] = value.get('value', 'No value')
                        results.append(result_info)

                    response_data = {'results': results}
                else:
                    response_data = {"error": "No results found."}
            else:
                response_data = {"error": f"Error {response.status_code}: {response.text}"}
    else:
        form = SparqlQueryForm()

    return render(request, 'sparql_query/query.html', {'form': form, 'response_data': response_data})
