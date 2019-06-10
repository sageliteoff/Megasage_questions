from django import forms

class SearchForm(forms.Form):
    searchInput_attrs = {
        "class":"search-bar",
        "placeholder":"search course.eg: ECO 101",
        "name": "search_input"
    }
    searchInput = forms.CharField(widget=forms.TextInput(attrs=searchInput_attrs))
