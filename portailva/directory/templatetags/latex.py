from django import template

register = template.Library()


@register.filter
def escape_latex_specials(value):
    return (value
            .replace('&', '\\&')
            .replace('#', '\\#')
            .replace('_', '\\_')
            .replace('\\', '\\backslash')
            .replace('€', '\\euro{}')
            .replace('$', '\\$')
            .replace('n°', '\\no')
            )

