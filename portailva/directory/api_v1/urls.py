from django.conf.urls import url

from .views import DirectoryAPIView, PrivateDirectoryAPIView

urlpatterns = [
    url('^private/$', PrivateDirectoryAPIView.as_view(), name='api-v1-directory-private'),
    url('^$', DirectoryAPIView.as_view(), name='api-v1-directory-index'),
]
