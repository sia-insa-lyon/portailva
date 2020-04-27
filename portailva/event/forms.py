import requests
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.utils.datetime_safe import datetime

from .models import Event, EventPrice


class EventForm(forms.ModelForm):
    short_description = forms.CharField(
        label="Description courte",
        help_text=str(Event._meta.get_field('short_description').max_length) + " caractères max.",
        widget=forms.Textarea(),
        max_length=Event._meta.get_field('short_description').max_length
    )

    begins_at = forms.DateTimeField(
        label="Date et heure de début",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        # widget=DateTimePicker(options=settings.PICKER_DATETIME_OPTIONS)

    )

    ends_at = forms.DateTimeField(
        label="Date et heure de fin",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        # widget=DateTimePicker(options=settings.PICKER_DATETIME_OPTIONS)
    )

    begin_publication_at = forms.DateTimeField(
        label="Date et heure de début de l'affichage sur les TV via Affichage",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        required=False
    )

    end_publication_at = forms.DateTimeField(
        label="Date et heure de fin de l'affichage sur les TV via Affichage",
        help_text="Format : " + settings.PICKER_DATETIME_OPTIONS['format'],
        required=False
    )

    class Meta(object):
        model = Event
        fields = ('type', 'name', 'short_description', 'description', 'place', 'begins_at', 'ends_at',
                  'website_url', 'logo_url', 'facebook_url', 'has_poster', 'begin_publication_at', 'end_publication_at',
                  'content_url', 'duration')

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'eventForm'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'

    def clean(self):
        super(EventForm, self).clean()
        ends_at = self.cleaned_data['ends_at']
        begins_at = self.cleaned_data['begins_at']

        if ends_at.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
            raise forms.ValidationError("Vous ne pouvez pas créer d'événement dans le passé.", code='invalidEnd')

        if begins_at >= ends_at:
            raise forms.ValidationError("La date de fin doit être ultérieure à la date de début.", code='invalidBegin')

        has_poster = self.cleaned_data['has_poster']

        if has_poster:
            begin_publication_at = self.cleaned_data['begin_publication_at']
            end_publication_at = self.cleaned_data['end_publication_at']

            if not begin_publication_at or not end_publication_at:
                if not begin_publication_at:
                    raise forms.ValidationError("Vous devez renseigner la date de début de publication.", code='missingBeginPubli')
                if not end_publication_at:
                    raise forms.ValidationError("Vous devez renseigner la date de fin de publication.", code='missingEndPubli')

            content_url = self.cleaned_data['content_url']
            duration = self.cleaned_data['duration']
            if not content_url or not duration:
                if not content_url:
                    raise forms.ValidationError("Vous devez renseigner la ressource à publier.", code='missingContent')
                if not duration:
                    raise forms.ValidationError("Vous devez renseigner la durée d'apparition de la publication.", code='missingDuration')

            if duration < 1:
                raise forms.ValidationError("La durée d'apparition de publication doit être de 1 s au minimum.", code='invalidDuration')

            if end_publication_at.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                raise forms.ValidationError("Vous ne pouvez pas publier d'événement dans le passé.", code='invalidEndPublication')

            if begin_publication_at >= end_publication_at:
                raise forms.ValidationError("La date de fin de publication doit être ultérieure à la date de début de publication.", code='invalidBeginPublication')

            if ends_at < end_publication_at:
                raise forms.ValidationError("Vous ne pouvez pas publier d'événement après la fin de ce dernier.", code='invalidEndPublicationWithBegin')

        return self.cleaned_data

    def save(self, commit=True):
        self.instance.association_id = self.association.id
        return super(EventForm, self).save(commit)


class EventPriceForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom du tarif",
        max_length=EventPrice._meta.get_field('name').max_length,
        widget=forms.TextInput(attrs={'placeholder': "Ex : plein tarif, Tarif VA, etc."})
    )
    price = forms.DecimalField(
        label="Tarif",
        initial=0.0,
        help_text="Valeur en €. Mettre 0 pour gratuit."
    )

    class Meta(object):
        model = EventPrice
        fields = ('name', 'price', 'is_va', 'is_variable',)

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super(EventPriceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'eventPriceForm'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'

    def save(self, commit=True):
        self.instance.event_id = self.event.id
        return super(EventPriceForm, self).save(commit)
