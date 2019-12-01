import math

from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract_absolute(value, arg):
    return math.fabs(value - arg)
