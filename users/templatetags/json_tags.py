import json
from django import template
register = template.Library()

@register.filter
def dicLen(data):
    return len(data)