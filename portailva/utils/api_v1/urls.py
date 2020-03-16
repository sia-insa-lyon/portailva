from django.conf.urls import url
from portailva.utils.api_v1.views import PlaceAPIView

urlpatterns = [
    url(r'^$', PlaceAPIView.as_view(), name='api-v1-place-index'),
]
