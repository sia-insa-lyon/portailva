from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract_absolute(value, arg):
    return value - arg if value - arg >= 0 else 0
