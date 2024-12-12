from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_sparql, name='query_sparql'),  # La vue de votre page de requête SPARQL
]
