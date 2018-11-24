from django.contrib import admin

# Register your models here.
from portailva.file.models import File, FileVersion, AssociationFile, FileType, FileFolder, ResourceFile


class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(File, FileAdmin)
admin.site.register(FileType)


class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'version', 'data')
    list_display_links = ('id', 'file')
    search_fields = ('file__name', 'version')
    list_per_page = 50


admin.site.register(FileVersion, FileVersionAdmin)

admin.site.register(AssociationFile)
admin.site.register(ResourceFile)


class FileFolderAdmin(admin.ModelAdmin):
    list_display = 'name', 'parent', 'position', 'is_writable', 'is_public'


admin.site.register(FileFolder, FileFolderAdmin)
