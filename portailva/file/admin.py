from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from portailva.file.models import File, FileVersion, AssociationFile, FileType, FileFolder, ResourceFile


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')
    list_per_page = 50


admin.site.register(File, FileAdmin)
admin.site.register(FileType)


class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'version', 'data')
    list_display_links = ('id', 'file')
    search_fields = ('file__name', 'version')
    list_per_page = 50


admin.site.register(FileVersion, FileVersionAdmin)


class AssociationFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'association', 'folder', 'created_at', 'link_file')
    list_display_links = ('name', 'association', 'folder')
    search_fields = ('association__name', 'name', 'folder__name')
    list_per_page = 50

    def link_file(self, obj):
        return format_html(
            '<a class="button" href="{}" rel="noreferrer noopener" target="_blank">Ouvrir</a>',
            reverse('file-view', args=[obj.uuid])
        )
    link_file.short_description = "Action"


admin.site.register(AssociationFile, AssociationFileAdmin)


class ResourceFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public')


admin.site.register(ResourceFile, ResourceFileAdmin)


class FileFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'position', 'is_writable', 'is_public')


admin.site.register(FileFolder, FileFolderAdmin)
