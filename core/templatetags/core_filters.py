"""
Custom template filters for Sibane ECD Academy.
Allows dictionary access in templates: {{ my_dict|dict_get:key }}
"""
from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Get a dictionary value by key in templates."""
    if isinstance(d, dict):
        return d.get(key)
    return None


@register.filter
def get_item(d, key):
    """Alias for dict_get — access dict by variable key."""
    if isinstance(d, dict):
        return d.get(key)
    return None
