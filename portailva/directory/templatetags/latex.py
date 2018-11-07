from django import template

register = template.Library()


@register.filter
def escape_latex_specials(value):
    return (value
            .replace('\\', '\\backslash{}')
            .replace('&', '\\&')
            .replace('#', '\\#')
            .replace('_', '\\_')
            .replace('€', '\\euro{}')
            .replace('$', '\\$')
            .replace('n°', '\\no{}')
            .replace('·', '.')
            .replace('\n\n', '\n')
            .replace('\n', '\n\n')
            )

