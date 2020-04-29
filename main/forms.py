from django import forms


class SearchForm(forms.Form):
    value = forms.CharField(max_length=100, help_text='Write some request')
