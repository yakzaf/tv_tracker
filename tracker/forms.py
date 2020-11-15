from django import forms


class SearchForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control',
                                    'name': 'q',
                                    'type': 'search',
                                    'placeholder': 'Search movies and TV shows'})
    q = forms.CharField(min_length=3, required=False, widget=widget, label='')
