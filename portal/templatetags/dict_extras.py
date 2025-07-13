from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """Get a value from a dictionary using a variable key"""
    return dictionary.get(key, 0)
