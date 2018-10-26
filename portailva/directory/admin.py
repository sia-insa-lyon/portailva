from django.contrib import admin

# Register your models here.
from portailva.directory.models import DirectoryEntry, OpeningHour


@admin.register(DirectoryEntry)
class DirectoryEntryAdmin(admin.ModelAdmin):
    list_display = 'id', 'asso_name', 'created_at', 'is_online'
    list_editable = 'is_online',
    list_display_links = 'id',
    search_fields = 'association__name',
    list_filter = 'is_online',
    date_hierarchy = 'created_at'
    ordering = 'id',

    def asso_name(self, obj):
        return obj.association.name

    asso_name.short_description = "Nom de l'association"
    asso_name.admin_order_field = 'association__name'


@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = 'id', 'asso_name', 'day', 'begins_at', 'ends_at', '_created_at'
    list_display_links = 'id',
    search_fields = 'directory_entry__association__name',
    list_filter = 'day',
    ordering = 'id',

    def asso_name(self, obj):
        return obj.directory_entry.association.name

    asso_name.short_description = "Nom de l'association"
    asso_name.admin_order_field = 'association__name'

    def _created_at(self, obj):
        return obj.directory_entry.created_at

    _created_at.short_description = "Créé le"
    _created_at.admin_order_field = 'directory_entry__created_at'


