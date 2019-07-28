from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView

from portailva.association.models import Association
from portailva.event.models import Event


class HomeView(ListView):
    model = Association
    context_object_name = 'associations'
    query = None
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.associations.count() == 1:
                return redirect('association-detail', request.user.associations.first().id)
        return super().dispatch(request, *args, **kwargs)

    @property
    def queryset(self):
        return (Association.objects
                .filter(is_validated=True)
                .filter(directory_entries__isnull=False)
                .filter(directory_entries__is_online=True)
                .distinct())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highlights'] = {}

        association_get_by_query = self.queryset.order_by('?')[:5]
        context['highlights']['association'] = association_get_by_query

        events = (Event.objects.filter(association__in=self.queryset)
                               .filter(is_online=True)
                               .filter(ends_at__gte=datetime.now())
                               .order_by('?')[:5])
        context['highlights']['events'] = events

        return context
