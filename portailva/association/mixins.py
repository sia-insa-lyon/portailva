from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from portailva.association.models import Association, Requirement


class AssociationMixin(LoginRequiredMixin):
    association = None

    def dispatch(self, request, *args, **kwargs):
        association_pk = int(self.kwargs.get('association_pk', None))
        self.association = get_object_or_404(Association, pk=association_pk)
        if not self.association.can_access(self.request.user):
            raise PermissionDenied

        return super(AssociationMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationMixin, self).get_context_data(**kwargs)
        context['association'] = self.association
        return context


class RequirementMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_requirement'):
            raise PermissionDenied
        return super(RequirementMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            requirement = Requirement.objects.get(id=self.kwargs.get('pk', None))
        except Requirement.DoesNotExist:
            raise Http404
        return requirement


class RequirementStaffMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        # Be sure that CUD operations are done by admin and only admin
        if not request.user.has_perm('association.admin_requirement') and not (request.user.is_active and request.user.is_staff):
            raise PermissionDenied
        return super(RequirementStaffMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            requirement = Requirement.objects.get(id=self.kwargs.get('pk', None))
        except Requirement.DoesNotExist:
            raise Http404
        return requirement