from django.conf.urls import url

from portailva.file.views.admin_files import FileListView
from portailva.file.views.admin_resources import UploadResourceView, CreateResourceFolderView, \
    ResourceFolderListView, ResourceFileDeleteView, ResourceFolderDeleteView
from portailva.file.views.association_files import AssociationFileTreeView, \
    AssociationFileUploadView, AssociationFileDeleteView, AssociationFileRenameView
from portailva.file.views.association_resources import AssocitationResourceView
from portailva.file.views.files import FileView

urlpatterns = [
    # File
    url('^file/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', FileView.as_view(), name='file-view'),

    # Association file
    url('^association/(?P<association_pk>\d+)/file/tree(?:/(?P<folder_pk>\d+))?/$', AssociationFileTreeView.as_view(),
        name='association-file-tree'),
    url('^association/(?P<association_pk>\d+)/resources(?:/(?P<folder_pk>\d+))?/$',
        AssocitationResourceView.as_view(), name='association-resource-tree'),
    url('^association/(?P<association_pk>\d+)/file/tree/(?P<folder_pk>\d+)/upload/$',
        AssociationFileUploadView.as_view(), name='association-file-upload'),
    url('^association/(?P<association_pk>\d+)/file/(?P<pk>\d+)/rename/$', AssociationFileRenameView.as_view(),
        name='association-file-rename'),
    url('^association/(?P<association_pk>\d+)/file/(?P<pk>\d+)/delete/$', AssociationFileDeleteView.as_view(),
        name='association-file-delete'),

    # Admin stuff
    url('^file/$', FileListView.as_view(), name='file-list'),
    url('^resources(?:/(?P<folder_pk>\d+))?$', ResourceFolderListView.as_view(), name='resource-folder-list'),
    url('^resources(?:/(?P<folder_pk>\d+))?/new_file$', UploadResourceView.as_view(), name='resource-upload'),
    url('^resources(?:/(?P<folder_pk>\d+))?/new$', CreateResourceFolderView.as_view(),
        name='resource-folder-create'),
    url('^resources(?:/(?P<folder_pk>\d+))?/file/(?P<pk>\d+)/delete$', ResourceFileDeleteView.as_view(),
        name='resource-file-delete'),
    url('^resources(?:/(?P<folder_pk>\d+))?/folder/(?P<pk>\d+)/delete$', ResourceFolderDeleteView.as_view(),
        name='resource-folder-delete'),
]
