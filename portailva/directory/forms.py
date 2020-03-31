from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings

from .models import DirectoryEntry, OpeningHour


class DirectoryEntryForm(forms.ModelForm):
    class Meta(object):
        model = DirectoryEntry
        fields = ['description', 'contact_address', 'phone', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'place']

    def __init__(self, *args, **kwargs):
        super(DirectoryEntryForm, self).__init__(*args, **kwargs)

        description_length = len(self.initial.get('description', ''))
        template_help_text = self.fields['description'].help_text

        self.fields['description'].help_text = template_help_text.format(description_length,
                                                                         's' if (description_length > 0) else '')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'
        self.helper.form_id = 'directoryEntryForm'


class OpeningHourForm(forms.ModelForm):
    begins_at = forms.TimeField(
        label="Heure d'ouverture",
        # widget=DateTimePicker(options=settings.PICKER_TIME_OPTIONS),
        help_text="Format : HH:MM"
    )

    ends_at = forms.TimeField(
        label="Heure de fermeture",
        # widget=DateTimePicker(options=settings.PICKER_TIME_OPTIONS),
        help_text="Format : HH:MM"
    )

    class Meta(object):
        model = OpeningHour
        fields = ['day', 'begins_at', 'ends_at']

    def __init__(self, *args, **kwargs):
        super(OpeningHourForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'
        self.helper.form_id = 'openingHourForm'

    def clean(self):
        super(OpeningHourForm, self).clean()
        begins_at = self.cleaned_data.get('begins_at', None)
        ends_at = self.cleaned_data.get('ends_at', None)
        if begins_at is None or ends_at is None:
            raise forms.ValidationError("Veuillez renseigner les horaires d'ouverture et de fermeture.",
                                        code='invalidTime')
        if begins_at > ends_at:
            raise forms.ValidationError("Les horaires renseignés sont incohérents, "
                                        "vérifiez que vous ouvrez bien avant de fermer sur ce créneau.",
                                        code='invalidBegin')
        if begins_at == ends_at:
            raise forms.ValidationError("Les horaires renseignés sont identiques, "
                                        "veuillez changer l'horaire d'ouverture ou de fermeture.",
                                        code='invalidEqual')
        return self.cleaned_data
