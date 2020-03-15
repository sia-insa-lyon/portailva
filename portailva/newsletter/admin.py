from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html
from portailva.newsletter.models import Article, Newsletter


def publish(modeladmin, request, queryset):
    queryset.update(validated=True)


publish.short_description = "Publier les articles sélectionnés"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'validated', 'type', 'created_at', 'updated_at', 'shortcut']
    list_filter = 'validated', 'type',
    ordering = ['title']
    actions = [publish]

    def shortcut(self, obj):
        return format_html(
            '<a class="button" href="{}" rel="noreferrer noopener" target="_blank">Voir</a>',
            reverse('association-article-detail', args=[obj.association_id, obj.id])
        )

    shortcut.short_description = "Action"

admin.site.register(Article, ArticleAdmin)
admin.site.register(Newsletter)
