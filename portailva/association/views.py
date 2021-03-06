from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .forms import AssociationForm, AssociationAdminForm, MandateForm, PeopleForm, RequirementForm
from .mixins import AssociationMixin, RequirementMixin, RequirementStaffMixin
from .models import Association, Mandate, People, Requirement, Accomplishment


class AssociationListView(LoginRequiredMixin, ListView):
    template_name = 'association/list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.admin_association'):
            raise PermissionDenied
        return super(AssociationListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Association.objects.all().order_by('-is_active', '-is_validated', 'name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssociationListView, self).get_context_data(**kwargs)
        return context


class AssociationDetailView(LoginRequiredMixin, DetailView):
    model = Association
    template_name = 'association/detail.html'
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(AssociationDetailView, self).dispatch(request, *args, **kwargs)


class AssociationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'association/update.html'
    form_class = AssociationForm
    model = Association
    object = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        if self.object.can_admin(request.user):
            self.form_class = AssociationAdminForm
        return super(AssociationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationUpdateView, self).get_context_data(**kwargs)
        context['association'] = self.object

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'association': self.object, 'form': form})

    def form_valid(self, form):
        self.object = form.save()

        if self.object.has_place and not self.object.room.is_room:
            self.object.room.is_room = True
            self.object.room.save()

        messages.add_message(self.request, messages.SUCCESS, "Les informations ont bien été mises à jour.")

        return redirect(reverse('association-detail', kwargs={'pk': self.object.id}))


class AssociationNewView(LoginRequiredMixin, CreateView):
    template_name = 'association/new.html'
    form_class = AssociationAdminForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.add_association') or \
                not request.user.has_perm('association.admin_association'):
            raise PermissionDenied
        return super(AssociationNewView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=AssociationAdminForm):
        return form_class(self.request.POST)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        association = form.save()
        association.save()

        if association.has_place and not association.room.is_room:
            association.room.is_room = True
            association.room.save()

        return redirect(reverse('association-list'))


class AssociationDeleteView(LoginRequiredMixin, DeleteView):
    model = Association
    template_name = 'association/delete.html'
    success_url = reverse_lazy('association-list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_admin(request.user):
            raise PermissionDenied
        return super(AssociationDeleteView, self).dispatch(request, *args, **kwargs)


# Mandates
class AssociationMandateListView(AssociationMixin, ListView):
    model = Mandate
    template_name = 'association/mandate/list.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationMandateListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Mandate.objects.all()\
            .prefetch_related('peoples')\
            .prefetch_related('peoples__role')\
            .filter(association_id=self.association.id)\
            .order_by('-begins_at')


class AssociationMandateChangePhoneVisibility(AssociationMixin, UpdateView):
    model = Mandate

    def get(self, request, *args, **kwargs):
        return redirect(reverse('association-mandate-list', kwargs={
            'association_pk': self.association.id
        }))

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_active:
                mandate_to_change = Mandate.objects.get(pk=self.kwargs['mandate_pk'])
                mandate_to_change.share_phone = not mandate_to_change.share_phone
                mandate_to_change.save()
            else:
                raise Exception('A non-active user try to change mandate phone visibility')
            return redirect(reverse('association-mandate-list', kwargs={
                'association_pk': self.association.id
            }))
        except Exception:
            raise Http404


class AssociationMandateNewView(AssociationMixin, CreateView):
    model = Mandate
    form_class = MandateForm
    template_name = 'association/mandate/new.html'

    def get_form(self, form_class=MandateForm):
        return form_class(self.request.POST, association=self.association)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(association=self.association),
            'association': self.association
        })

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {
            'form': form,
            'association': self.association
        })

    def form_valid(self, form):
        Mandate.objects.create(
            begins_at=form.cleaned_data.get('begins_at'),
            ends_at=form.cleaned_data.get('ends_at'),
            association_id=self.association.id
        )

        return redirect(reverse('association-mandate-list', kwargs={
            'association_pk': self.association.id
        }))


class AssociationMandateMixin(AssociationMixin):
    mandate = None
    success_url = None

    def dispatch(self, request, *args, **kwargs):
        mandate = Mandate.objects.all()\
            .filter(association_id=kwargs.get('association_pk'))\
            .order_by('-begins_at')[:1]
        if len(mandate) < 1:
            raise Http404
        if mandate[0].id != int(kwargs.get('mandate_pk', None)):
            raise Http404
        self.mandate = mandate[0]
        self.success_url = reverse('association-mandate-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationMandateMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationMandateMixin, self).get_context_data(**kwargs)
        context['mandate'] = self.mandate
        return context


class AssociationMandatePeopleNewView(AssociationMandateMixin, CreateView):
    model = People
    form_class = PeopleForm
    template_name = 'association/mandate/people_new.html'

    def form_valid(self, form):
        people = form.save(commit=False)
        people.mandate = self.mandate
        people.save()
        return redirect(reverse('association-mandate-list', kwargs={
            'association_pk': self.association.id
        }))


class AssociationMandatePeopleMixin(AssociationMandateMixin):
    def get_object(self, queryset=None):
        try:
            # We make sure mandate_pk provided in url matches with mandate linked to people
            people = People.objects.get(id=self.kwargs.get('pk', None))
            if people.mandate_id != self.mandate.id:
                raise Http404
        except People.DoesNotExist:
            raise Http404
        return people


class AssociationMandatePeopleUpdateView(AssociationMandatePeopleMixin, UpdateView):
    model = People
    form_class = PeopleForm
    template_name = 'association/mandate/people_edit.html'


class AssociationMandatePeopleDeleteView(AssociationMandateMixin, DeleteView):
    model = People
    template_name = 'association/mandate/people_delete.html'


class AssociationRequirementListView(AssociationMixin, ListView):
    model = Requirement
    template_name = 'association/requirement/list.html'

    def get_queryset(self):
        return self.model.objects.get_all_active()


class AssociationRequirementAchieveView(AssociationMixin, SingleObjectMixin, View):
    model = Requirement
    http_method_names = ['post']
    object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('association.achieve_requirement'):
            raise PermissionDenied
        return super(AssociationRequirementAchieveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # We only can achieve accomplishment or room typed requirements
        if self.object.type != 'accomplishment' and self.object.type != 'room':
            return Http404

        try:
            accomplishment = Accomplishment.objects.get(
                association_id=self.association.id,
                requirement_id=self.object.id)
            accomplishment.delete()
        except Accomplishment.DoesNotExist:
            Accomplishment.objects.create(association_id=self.association.id, requirement_id=self.object.id)
        finally:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RequirementListView(RequirementMixin, ListView):
    model = Requirement
    template_name = 'association/requirement/admin_list.html'

    def get_queryset(self):
        return self.model.objects.get_all_active()


class RequirementDetailView(RequirementMixin, DetailView):
    model = Requirement
    template_name = 'association/requirement/detail.html'

    def get_context_data(self, **kwargs):
        context = super(RequirementDetailView, self).get_context_data(**kwargs)
        # Check if we need to remove association without room
        if context['object'].type == 'room':
            context.update({
                'associations': Association.objects.filter(is_active=True).filter(has_place=True).order_by('name')
            })
        else:
            context.update({
                'associations': Association.objects.filter(is_active=True).order_by('name')
            })
        return context


class RequirementNewView(RequirementStaffMixin, CreateView):
    model = Requirement
    form_class = RequirementForm
    template_name = 'association/requirement/new.html'

    def form_valid(self, form):
        requirement = form.save(commit=False)
        requirement.save()
        return redirect(reverse('requirement-list'))


class RequirementUpdateView(RequirementStaffMixin, UpdateView):
    model = Requirement
    form_class = RequirementForm
    template_name = 'association/requirement/update.html'

    def form_valid(self, form):
        requirement = form.save(commit=False)
        requirement.save()
        return redirect(reverse('requirement-detail', kwargs={
            'pk': requirement.id
        }))


class RequirementDeleteView(RequirementStaffMixin, DeleteView):
    model = Requirement
    template_name = 'association/requirement/delete.html'
    success_url = reverse_lazy('requirement-list')


class GlobalDirectoryView(LoginRequiredMixin, ListView):
    model = Association
    template_name = 'association/global_directory.html'

    def get_queryset(self):
        return Association.objects.filter(is_active=True).order_by('name')
