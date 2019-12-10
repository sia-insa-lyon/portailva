import shutil
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from portailva import settings
from portailva.association.models import Association, Requirement
from portailva.directory.models import DirectoryEntry
from portailva.event.models import Event


class HomeView(TemplateView):
    model = Association
    context_object_name = 'associations'
    query = None
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @property
    def queryset(self):
        return (Association.objects
                .filter(is_validated=True)
                .filter(is_active=True)
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
        context['associations'] = list(association_get_by_query) + list(Association.objects.filter(events__in=events))

        return context


@method_decorator(login_required, name='dispatch')
class DashBoardView(TemplateView):
    context_object_name = 'admin'
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_requirement'):
            raise PermissionDenied
        return super(DashBoardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['alert'] = {}
        # Quelle asso n'a pas d'utilisateur ?
        context['alert']['user'] = (Association.objects.filter(is_active=True)
                                    .filter(users__isnull=True)
                                    .order_by('name', 'acronym'))

        # Quelle asso a un utilisateur du staff ou un super-utilisateur dans ses utilisateurs ?
        context['alert']['user_privilege'] = (Association.objects.filter(is_active=True)
                                              .filter(users__in=User.objects.filter(is_active=True)
                                                      .filter(Q(is_staff=True) | Q(is_superuser=True)))
                                              .order_by('name', 'acronym')
                                              .distinct())

        # Quelle asso n'a pas de référent CVA ?
        context['alert']['no_referent'] = Association.objects.filter(is_active=True) \
            .filter(moderated_by__isnull=True).order_by('name')

        # Quelle asso a un utilisateur qui ne s'est pas connecté depuis au moins 180 jours ?
        context['alert']['disconnected'] = (Association.objects.filter(is_active=True)
                                            .filter(users__last_login__lte=datetime.now() - timedelta(days=180))
                                            .order_by('name', 'acronym')
                                            .distinct())

        context['alert']['sum'] = (len(context['alert']['user']) + len(context['alert']['user_privilege'])
                                   + len(context['alert']['no_referent']) + len(context['alert']['disconnected']))
        disk_stats = shutil.disk_usage(settings.MEDIA_ROOT)
        # Get size in MB. Warning: theses stats concern the whole disk
        context['alert']['disk_free'] = int(disk_stats.free / 1000 ** 2)
        context['alert']['disk_used'] = int(disk_stats.used / 1000 ** 2)
        context['alert']['disk_total'] = int(disk_stats.total / 1000 ** 2)

        context['events'] = Event.objects.filter(is_online=False)
        context['events_stats'] = {}
        context['events_stats']['published'] = (Event.objects.filter(is_online=True)
                                                .filter(begins_at__gte=datetime.now() - timedelta(days=180))
                                                .count())

        context['events_stats']['unpublished'] = len(context['events'])

        context['directory'] = DirectoryEntry.objects.filter(is_online=False).order_by('updated_at')

        context['association_stats'] = {}
        context['association_stats']['members'] = (Association.objects.filter(is_active=True)
                                                   .aggregate(Sum('all_members_number'), Sum('active_members_number')))

        context['association_stats']['place'] = (Association.objects.filter(is_active=True)
                                                 .filter(has_place=True)
                                                 .count())

        list_active_asso = Association.objects.filter(is_active=True).order_by('name', 'acronym')
        context['association_stats']['active'] = len(list_active_asso)

        context['requirement_stats'] = {}
        list_requirement = []
        for req in Requirement.objects.get_all_active():
            validated = 0
            for asso in list_active_asso:
                if req.is_achieved(asso.id):
                    validated += 1
            list_requirement.append({'id': req.id, 'name': req.name, 'type': req.type, 'validate': validated})

        context['requirement_stats'] = list_requirement
        context['supervised_assos'] = (Association.objects.filter(is_active=True)
                                       .filter(moderated_by=self.request.user.id)
                                       .order_by('name', 'acronym'))

        return context
