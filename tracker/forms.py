from django import forms


class SearchForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control',
                                    'name': 'q',
                                    'type': 'search',
                                    'placeholder': 'Search...'})
    q = forms.CharField(min_length=3, required=False, widget=widget, label='')
