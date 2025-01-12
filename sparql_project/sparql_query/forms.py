from django import forms

class SparqlQueryForm(forms.Form):
    sparql_query = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), label="SPARQL Query")
