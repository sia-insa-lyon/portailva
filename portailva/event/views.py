from datetime import datetime, timedelta

import pytz
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
import icalendar
from icalendar import vText, vGeo

from portailva.association.mixins import AssociationMixin
from portailva.event.forms import EventForm, EventPriceForm
from portailva.event.mixins import AssociationEventMixin, AssociationEventPriceMixin
from .models import Event, EventPrice


class AssociationEventListView(AssociationMixin, ListView):
    model = Event
    template_name = 'event/association_event_list.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationEventListView, self).get_context_data(**kwargs)
        context.update({
            'past_events': self.get_past_events()
        })
        return context

    def get_queryset(self):
        return Event.objects.all()\
            .select_related('type')\
            .filter(association_id=self.association.id)\
            .filter(ends_at__gte=datetime.now())\
            .order_by('begins_at')

    def get_past_events(self):
        return Event.objects.all()\
            .select_related('type')\
            .filter(association_id=self.association.id)\
            .filter(ends_at__lt=datetime.now())\
            .order_by('-ends_at')


class AssociationEventDetailView(AssociationMixin, DetailView):
    model = Event
    template_name = 'event/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().association.can_access(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationEventDetailView, self).get_context_data()
        context.update({
            'can_update': self.object.can_update(self.request.user),
            'can_delete': self.object.can_delete(self.request.user)
        })
        return context


class AssociationEventNewView(AssociationMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/new.html'

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventNewView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationEventNewView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationEventUpdateView(AssociationMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/update.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_update(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Event is offline after update to enforce a new validation
        self.object = form.save(commit=False)
        self.object.is_online = False
        self.object.save()

        return redirect(reverse('association-event-list', kwargs={
            'association_pk': self.association.id
        }))

    def get_form_kwargs(self):
        kwargs = super(AssociationEventUpdateView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationEventDeleteView(AssociationMixin, DeleteView):
    model = Event
    template_name = 'event/delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_delete(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-event-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationEventDeleteView, self).dispatch(request, *args, **kwargs)


class AssociationEventPriceNewView(AssociationEventMixin, CreateView):
    model = EventPrice
    form_class = EventPriceForm
    template_name = 'event/price/new.html'

    def get(self, request, *args, **kwargs):
        if not self.event.can_update(request.user):
            raise Http404
        return super(AssociationEventPriceNewView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.event.can_update(request.user):
            raise Http404
        return super(AssociationEventPriceNewView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationEventPriceNewView, self).get_form_kwargs()
        kwargs.update({
            'event': self.event
        })

        return kwargs

    def get_success_url(self):
        return reverse('association-event-detail', kwargs={
            'association_pk': self.association.id,
            'pk': self.event.id
        })


class AssociationEventPriceUpdateView(AssociationEventPriceMixin, UpdateView):
    model = EventPrice
    form_class = EventPriceForm
    template_name = 'event/price/update.html'


class AssociationEventPriceDeleteView(AssociationEventPriceMixin, DeleteView):
    model = EventPrice
    template_name = 'event/price/delete.html'


class AssociationEventPublishView(AssociationEventMixin, TemplateView):
    model = Event
    template_name = 'event/publish.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('event.admin_event'):
            raise PermissionDenied
        self.object = self.get_object()
        if self.object.is_online:
            raise Http404
        return super(AssociationEventPublishView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object.is_online = True
        self.object.save()
        return redirect(reverse('association-event-detail', kwargs={
            'association_pk': self.association.id,
            'pk': self.event.id
        }))

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('event_pk'))


class EventCalendarPublicView(ListView):
    model = Event
    template_name = 'event/calendar_public.html'

    def get_queryset(self):
        return {
            'all_events': Event.objects.filter(is_online=True)
            .filter(begins_at__gte=datetime.now() - timedelta(days=90))
            .order_by('begins_at'),

            'recent_events': Event.objects.filter(is_online=True)
            .filter(begins_at__gte=datetime.now())
            .order_by('begins_at')[:8]
        }


class EventDetailView(DetailView):
    model = Event
    template_name = 'event/public_detail.html'

    def get_queryset(self):
        return super().get_queryset()


class AllEventsCalendarView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        events = (Event.objects
                  .filter(is_online=True)
                  .filter(begins_at__gte=datetime.now() - timedelta(days=90)))

        cal = icalendar.Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//PortailVA events calendar//mxm.dk//')
        tz = pytz.timezone('Europe/Paris')

        for event in events:
            ev = icalendar.Event()
            if event.association.acronym:
                ev.add('summary', event.name + ' (' + event.association.acronym+ ')')
            else:
                ev.add('summary', event.name + ' (' + event.association.name+ ')')
            ev.add('description', event.description)
            # Use vText to prevent iCalendar to handle the string as a dictionary and not as a text
            # See https://icalendar.readthedocs.io/en/latest/usage.html#example
            ev.add('categories', vText(event.type.name))
            ev.add('dtstart', event.begins_at.replace(tzinfo=tz))
            ev.add('dtend', event.ends_at.replace(tzinfo=tz))
            if event.place:
                ev.add('location', event.place.name)
                ev.add('geo', vGeo([event.place.lat, event.place.long]))

            ev.add('uid', event.id)
            cal.add_component(ev)

        response = HttpResponse(content_type='text/calendar')
        response.write(cal.to_ical().replace(b'\r\n', b'\n').strip())
        return response
