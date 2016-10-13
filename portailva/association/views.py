from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from portailva.association.forms import AssociationForm, AssociationAdminForm
from portailva.association.models import Association


class AssociationListView(ListView):
    template_name = 'association/list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('association.can_admin_association'):
            raise PermissionDenied
        return super(AssociationListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Association.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssociationListView, self).get_context_data(**kwargs)
        return context


class AssociationDetailView(DetailView):
    model = Association
    template_name = 'association/detail.html'
    object = None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_access(request.user):
            raise PermissionDenied
        return super(AssociationDetailView, self).get(request, *args, **kwargs)


class AssociationUpdateView(UpdateView):
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

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.create_form(self.form_class, **{
            'name': self.object.name,
            'category': self.object.category,
            'acronym': self.object.acronym,
            'description': self.object.description,
            'is_active': self.object.is_active
        })

        return render(request, self.template_name, {'association': self.object, 'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'association': self.object, 'form': form})

    def create_form(self, form_class, **kwargs):
        return form_class(initial=kwargs)

    def get_form(self, form_class=None):
        return form_class(self.request.POST)

    def form_valid(self, form):
        self.object.name = form.data.get('name')
        self.object.category_id = form.data.get('category')
        self.object.acronym = form.data.get('acronym')
        self.object.description = form.data.get('description')

        # Admin form
        if self.form_class is AssociationAdminForm:
            self.object.is_active = False if not form.data.get('is_active') else True

        self.object.save()

        return redirect(reverse('association-detail', kwargs={'pk': self.object.id}))


class AssociationNewView(CreateView):
    template_name = 'association/new.html'
    form_class = AssociationAdminForm

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
        association = Association()
        association.name = form.data.get('name')
        association.category_id = form.data.get('category')
        association.acronym = form.data.get('acronym')
        association.description = form.data.get('description')
        association.is_active = form.data.get('is_active')
        association.save()

        return redirect(reverse('association-list'))


class AssociationDeleteView(DeleteView):
    model = Association
    template_name = 'association/delete.html'
    success_url = reverse_lazy('association-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_admin(request.user):
            raise PermissionDenied
        return super(AssociationDeleteView, self).dispatch(request, *args, **kwargs)
