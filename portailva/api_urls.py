from django.conf.urls import url, include

urlpatterns = [
    # API v1
    url(r'^v1/directory/', include('portailva.directory.api_v1.urls')),
    url(r'^v1/events/', include('portailva.event.api_v1.urls')),
    url(r'^v1/places/', include('portailva.utils.api_v1.urls'))
]
