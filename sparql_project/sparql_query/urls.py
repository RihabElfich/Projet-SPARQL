from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_sparql, name='query_sparql'),  # La vue de votre page de requête SPARQL
    path('visualiser-graphe/', views.afficher_graphe, name='afficher_graphe'),
     path('api/get_graph_data/', views.get_graph_data, name='get_graph_data'),
]
