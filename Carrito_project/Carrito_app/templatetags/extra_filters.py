from django import template

register = template.Library()

@register.filter
def split(value, arg):
    if value is None:
        return []
    return value.split(arg)

@register.filter
def trim(value):
    if value is None:
        return ''
    return value.strip()