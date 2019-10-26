from django.contrib.admin import ModelAdmin, register

from portailva.utils.models import Place


@register(Place)
class PlaceAdmin(ModelAdmin):
    list_display = [
        'name',
        'lat',
        'long',
    ]
