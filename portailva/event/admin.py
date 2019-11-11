from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from portailva.event.models import EventType, Event, EventPrice


def publish(modeladmin, request, queryset):
    queryset.update(is_online=True)


publish.short_description = "Publier les évènements sélectionnés"


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_online', 'type', 'begins_at', 'ends_at', 'short_cut']
    list_filter = 'is_online', 'type',
    ordering = ['name']
    actions = [publish]

    def short_cut(self, obj):
        return format_html(
            '<a class="button" href="{}" rel="noreferrer noopener" target="_blank">Voir</a>',
            reverse('association-event-detail', args=[obj.association_id, obj.id])
        )

    short_cut.short_description = "Action"


admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPrice)
