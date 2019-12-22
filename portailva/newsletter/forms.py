from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.db.models import Count
import datetime

from portailva.event.models import Event
from .models import Article, Newsletter


class ArticleForm(forms.ModelForm):
    class Meta(object):
        model = Article
        fields = ('title', 'featured_image', 'short_content', 'content',)

    short_content = forms.CharField(widget=forms.Textarea, label="Brève de l'article",
                                    help_text="Ce texte est affiché dans la newsletter VA. Il est limité à 255 "
                                              "caractères. Les retours à la ligne sont tolérés.")

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'articleForm'

    def save(self, commit=True):
        self.instance.association_id = self.association.id
        return super(ArticleForm, self).save(commit)


class NewsletterForm(forms.ModelForm):
    class Meta(object):
        model = Newsletter
        fields = ('title', 'sent', 'articles', 'events')

    events = forms.ModelMultipleChoiceField

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'newsletterForm'

        # Can't use directly a slice because the queryset is filtered again afterwise,
        # So we get the pk of the last 8 articles and filter using this list (avoids using splice directly)
        pks = Article.objects.order_by('-created_at').values('pk')[:8]
        self.fields['articles'].queryset = Article.objects.filter(pk__in=pks)

        self.fields['events'].queryset = Event.objects.filter(ends_at__gt=
                                                              datetime.datetime.today() - datetime.timedelta(days=1))\
            .order_by('begins_at')
