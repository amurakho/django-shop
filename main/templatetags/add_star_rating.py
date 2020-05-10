from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def add_star_rating(rating):
    html = '<span class="fa fa-star checked"></span>' * rating
    html += '<span class="fa fa-star"></span>' * (5 - rating)
    return mark_safe(html)
