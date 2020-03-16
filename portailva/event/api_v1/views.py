import datetime

from django.db.models import Q
from django.http import Http404
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from portailva.event.api_v1.serializers import EventSerializer, EventTypeSerializer
from portailva.event.models import Event, EventType


class EventListAPIView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Event.objects.get_online()
        since = self.request.query_params.get('since', None)
        until = self.request.query_params.get('until', None)
        asso_id = self.request.query_params.get('association_id', None)
        type_id = self.request.query_params.get('type_id', None)
        place_id = self.request.query_params.get('place_id', None)

        if since is None and until is None:
            # We return event for the next two days
            since = datetime.datetime.now().strftime('%Y-%m-%d')
            until = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        if since is not None and until is None:
            try:
                since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__lte=since_date) & Q(begins_at__gte=since_date)) |
                    (Q(begins_at__gte=since_date))
                )
            except ValueError:
                raise ParseError("Bad format for since parameter. Accepted format : %Y-%m-%d.")
        elif since is None and until is not None:
            try:
                until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__lte=until_date) & Q(ends_at__gte=until_date)) |
                    (Q(ends_at__lte=until_date))
                )
            except ValueError:
                raise ParseError("Bad format for until parameter. Accepted format : %Y-%m-%d.")
        else:
            try:
                since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
                until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
                queryset = queryset.filter(
                    (Q(begins_at__gte=since_date) & Q(begins_at__lte=until_date)) |
                    (Q(ends_at__gte=since_date) & Q(ends_at__lte=until_date)) |
                    (Q(begins_at__lte=since_date) & Q(ends_at__gte=until_date))
                )
            except ValueError:
                raise ParseError("Bad format for since/until parameters. Accepted format : %Y-%m-%d.")

        if asso_id is not None:
            queryset = queryset.filter(association__id=asso_id)

        if type_id is not None:
            queryset = queryset.filter(type_id=type_id)

        if place_id is not None:
            queryset = queryset.filter(place__in=place_id)

        return queryset


class EventByIdAPIView(RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        try:
            return Event.objects.get(id=self.kwargs.get('events_pk'))
        except IndexError:
            raise Http404


class EventTypeAPIView(ListAPIView):
    serializer_class = EventTypeSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return EventType.objects.all()
