from django.contrib import admin

# Register your models here.
from portailva.directory.models import DirectoryEntry, OpeningHour

admin.site.register(OpeningHour)

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


