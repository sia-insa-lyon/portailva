from django.contrib import admin
from .models import Category, Association, Mandate, PeopleRole, People, Requirement, Accomplishment


def publish_phone(modeladmin, request, queryset):
    queryset.update(share_phone=True)


publish_phone.short_description = "Publier les numéros des mandats sélectionnés"


def hide_phone(modeladmin, request, queryset):
    queryset.update(share_phone=False)


hide_phone.short_description = "Cacher les numéros des mandats sélectionnés"


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'acronym', 'category', 'active_members_number', 'is_active', 'is_validated', 'has_place'
    list_editable = 'acronym', 'category', 'active_members_number', 'is_active', 'is_validated', 'has_place'
    list_display_links = 'name',
    search_fields = 'name', 'acronym',
    list_filter = 'category', 'is_active', 'is_validated', 'has_place'
    ordering = 'name', 'id'


@admin.register(Mandate)
class AssociationMandateAdmin(admin.ModelAdmin):
    list_display = ('id', 'association', 'begins_at', 'ends_at', 'share_phone')
    list_display_links = ('id', 'association')
    search_fields = ('id', 'association__name')
    list_per_page = 50
    actions = [publish_phone, hide_phone]


admin.site.register(Category)
admin.site.register(PeopleRole)
admin.site.register(People)
admin.site.register(Requirement)
admin.site.register(Accomplishment)
