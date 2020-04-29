from django.template import Library

from main import forms


register = Library()


@register.simple_tag
def get_search_form():
    search_form = forms.SearchForm
    return search_form


