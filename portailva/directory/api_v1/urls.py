from django.conf.urls import url

from .views import DirectoryAPIView, PrivateDirectoryAPIView, PublicDirectoryByIdAPIView

urlpatterns = [
    url('^private/$', PrivateDirectoryAPIView.as_view(), name='api-v1-directory-private'),
    url('^(?P<association_pk>\d+)/$', PublicDirectoryByIdAPIView.as_view(), name='api-v1-directory-detail'),
    url('^$', DirectoryAPIView.as_view(), name='api-v1-directory-index'),
]
