from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView
from datetime import datetime, timedelta

from portailva.association.mixins import AssociationMixin
from portailva.newsletter.forms import ArticleForm, NewsletterForm
from portailva.newsletter.models import Article, Newsletter


class AssociationArticleListView(AssociationMixin, ListView):
    model = Article
    template_name = 'newsletter/article/list.html'

    def get_context_data(self, **kwargs):
        context = super(AssociationArticleListView, self).get_context_data()
        context.update({
            'to_validate': Article.objects.filter(association=self.association)
                .filter(validated=False)
                .order_by('-updated_at'),
            'validated': Article.objects.filter(association=self.association)
                .filter(validated=True)
                .order_by('-updated_at')
        })
        return context


class AssociationArticleNewView(AssociationMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'newsletter/article/new.html'

    def get_success_url(self):
        return reverse('association-article-detail', kwargs={'association_pk': self.association.id, 'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse('association-article-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationArticleNewView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AssociationArticleNewView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationArticleUpdateView(AssociationMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'newsletter/article/update.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().can_update(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-article-detail', kwargs={
            'association_pk': kwargs.get('association_pk'),
            'pk': kwargs.get('pk'),
        })
        return super(AssociationArticleUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Event is offline after update to enforce a new validation
        self.object = form.save(commit=False)
        self.object.validated = False
        self.object.save()

        return redirect(reverse('association-article-detail', kwargs={
            'association_pk': self.association.id,
            'pk': self.object.id
        }))

    def get_form_kwargs(self):
        kwargs = super(AssociationArticleUpdateView, self).get_form_kwargs()
        kwargs.update({
            'association': self.association
        })

        return kwargs


class AssociationArticlePublishView(AssociationMixin, TemplateView):
    model = Article
    template_name = 'newsletter/article/publish.html'
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('article.admin_article'):
            raise PermissionDenied
        self.object = self.get_object()
        if self.object.validated:
            raise Http404
        return super(AssociationArticlePublishView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object.validated = True
        self.object.save()
        return redirect(reverse('association-article-detail', kwargs={
            'association_pk': self.association.id,
            'pk': self.object.id
        }))

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('article_pk'))


class AssociationArticleDetailView(AssociationMixin, DetailView):
    model = Article
    template_name = 'newsletter/article/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().association.can_access(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssociationArticleDetailView, self).get_context_data()
        context.update({
            'can_update': self.object.can_update(self.request.user),
            'can_delete': self.object.can_delete(self.request.user),
            'can_publish': self.object.can_publish(self.request.user)
        })
        return context


class AssociationArticleDeleteView(AssociationMixin, DeleteView):
    model = Article
    template_name = 'newsletter/article/delete.html'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.can_delete(request.user):
            raise PermissionDenied
        self.success_url = reverse('association-article-list', kwargs={
            'association_pk': kwargs.get('association_pk')
        })
        return super(AssociationArticleDeleteView, self).dispatch(request, *args, **kwargs)


class ValidatedArticleListView(ListView):
    model = Article
    template_name = 'newsletter/article/list_public.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(validated=True).filter(
            updated_at__gte=datetime.now() - timedelta(days=180)).order_by('-updated_at')

    def dispatch(self, request, *args, **kwargs):
        return super(ValidatedArticleListView, self).dispatch(request, *args, **kwargs)


class ValidatedArticleDetailView(DetailView):
    model = Article
    template_name = 'newsletter/article/detail_public.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.validated:
            raise Http404
        return super(ValidatedArticleDetailView, self).dispatch(request, *args, **kwargs)


class NewsletterListView(ListView):
    model = Newsletter
    template_name = 'newsletter/newsletter/list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterListView, self).dispatch(request, *args, **kwargs)


class NewsletterNewView(CreateView):
    model = Newsletter
    template_name = 'newsletter/newsletter/new.html'
    form_class = NewsletterForm

    def get_success_url(self):
        return reverse('newsletter-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterNewView, self).dispatch(request, *args, **kwargs)


class NewsletterUpdateView(CreateView):
    model = Newsletter
    template_name = 'newsletter/newsletter/update.html'
    form_class = NewsletterForm
    object = None

    def get_success_url(self):
        return reverse('newsletter-detail', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewsletterUpdateView, self).get_context_data()
        context.update({'newsletter_title': self.get_object().title})

        return context


class NewsletterDetailView(DetailView):
    model = Newsletter
    template_name = 'newsletter/newsletter/detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsletterDetailView, self).get_context_data()
        context.update({
            'can_update': self.request.user.has_perm('newsletter.admin_newsletter'),
            'can_delete': self.request.user.has_perm('newsletter.admin_newsletter')
        })
        return context


class NewsletterOnlineView(DetailView):
    model = Newsletter
    template_name = 'newsletter/email/email.html'

    def get_context_data(self, **kwargs):
        context = super(NewsletterOnlineView, self).get_context_data()
        context.update({
            'articles': kwargs['object'].articles.all(),
            'events': kwargs['object'].events.order_by('begins_at').all(),
            'top_articles': kwargs['object'].articles.filter(type='FEATURED'),
            'classic_articles': kwargs['object'].articles.filter(type='CLASSIC')
        })
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'newsletter/email/article.html'


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    template_name = 'newsletter/newsletter/delete.html'

    def get_success_url(self):
        return reverse('newsletter-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('newsletter.admin_newsletter'):
            raise PermissionDenied
        return super(NewsletterDeleteView, self).dispatch(request, *args, **kwargs)
