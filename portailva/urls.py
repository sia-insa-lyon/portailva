"""portailva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from portailva.pages.views import HomeView, DashBoardView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('portailva.association.urls')),
    url(r'^member/', include('portailva.member.urls')),
    url(r'', include('portailva.directory.urls')),
    url(r'', include('portailva.file.urls')),
    url(r'', include('portailva.utils.urls')),
    url(r'', include('portailva.event.urls')),
    url(r'', include('portailva.newsletter.urls')),
    url(r'export/', include('portailva.export.urls')),

    # REST API
    url(r'^api/', include('portailva.api_urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^dashboard/$', DashBoardView.as_view(), name='admin-dashboard'),
    url(r'^$', HomeView.as_view(), name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
