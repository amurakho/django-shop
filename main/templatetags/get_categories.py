from django.template import Library

from main import models


register = Library()


@register.simple_tag
def get_categories():
    cat_list = models.Category.objects.all()
    return cat_list


