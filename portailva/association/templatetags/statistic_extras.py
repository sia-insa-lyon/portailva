import math

from django import template

register = template.Library()


@register.filter(name='percent')
def percentage(value, arg):
    return math.floor(math.fabs((arg / value) * 10000))/100


@register.filter(name='subtract')
def subtract_absolute(value, arg):
    return math.fabs(value - arg)
