from colorhash import ColorHash
from django import template

register = template.Library()


@register.filter
def colorhash(value):
    return ColorHash(value).hex
