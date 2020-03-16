from django.conf.urls import url

from portailva.event.api_v1.views import EventListAPIView, EventByIdAPIView, EventTypeAPIView

urlpatterns = [
    url(r'^$', EventListAPIView.as_view(), name='api-v1-event-index'),
    url('^(?P<events_pk>\d+)/$', EventByIdAPIView.as_view(), name='api-v1-event-detail'),
    url('^type/$', EventTypeAPIView.as_view(), name='api-v1-event-type'),
]
