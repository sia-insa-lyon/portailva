from django.contrib.admin import ModelAdmin, register

from portailva.utils.models import Place


def set_is_room(modeladmin, request, queryset):
    queryset.update(is_room=True)


def unset_is_room(modeladmin, request, queryset):
    queryset.update(is_room=False)


set_is_room.short_description = "Définir comme local associatif"
unset_is_room.short_description = "Retirer le statut de local association"


@register(Place)
class PlaceAdmin(ModelAdmin):
    list_display = [
        'name',
        'lat',
        'long',
        'is_room'
    ]
    actions = [set_is_room, unset_is_room]
