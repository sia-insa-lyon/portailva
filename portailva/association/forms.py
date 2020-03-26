import json
from datetime import datetime

from crispy_forms.helper import FormHelper
from django import forms
from django.core.validators import EMPTY_VALUES

from .models import Association, Mandate, People, Requirement
from ..file.models import FileFolder


class AssociationForm(forms.ModelForm):
    class Meta:
        fields = ['category', 'name', 'acronym', 'description',
                  'active_members_number', 'all_members_number',
                  'logo_url', 'iban', 'bic', 'rna', 'siren', 'created_officially_at']
        model = Association

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'
        self.helper.form_id = 'associationForm'


class AssociationAdminForm(AssociationForm):
    class Meta(AssociationForm.Meta):
        fields = AssociationForm.Meta.fields + ['commentary', 'is_active', 'is_validated', 'has_place', 'room']

    def clean(self):
        super(AssociationAdminForm, self).clean()
        has_place = self.cleaned_data.get('has_place', False)
        if has_place:
            room = self.cleaned_data.get('room', None)
            if room in EMPTY_VALUES:
                raise forms.ValidationError("Vous avez déclaré que l'association dispose d'un local, veuillez "
                                            "renseigner le local correspondant !", code='invalidRoom')
        return self.cleaned_data


class MandateForm(forms.Form):
    begins_at = forms.DateField(
        label="Début de mandat",
        # widget=DateTimePicker(options=settings.PICKER_DATE_OPTIONS),
        help_text="Format : JJ/MM/AAAA"
    )

    ends_at = forms.DateField(
        label="Fin de mandat",
        # widget=DateTimePicker(options=settings.PICKER_DATE_OPTIONS),
        help_text="Format : JJ/MM/AAAA"
    )

    def __init__(self, *args, **kwargs):
        self.association = kwargs.pop('association', None)
        super(MandateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'mandateForm'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'

    def clean(self):
        super(MandateForm, self).clean()
        begins_at = self.cleaned_data.get('begins_at')
        ends_at = self.cleaned_data.get('ends_at')

        if not begins_at or not ends_at:
            raise forms.ValidationError("Erreur dans la date de début ou de fin.", code='invalidInterval')

        # We ensure begins_at is strictly before ends_at
        if begins_at >= ends_at:
            raise forms.ValidationError("La date de fin ne peut ni être égale ni être antérieure à la date de début.",
                                        code='invalidBegin')

        # We ensure there is no other mandate during the same time as defined by the user
        association_mandates = Mandate.objects.all().filter(association_id=self.association.id)
        for mandate in association_mandates:
            if (begins_at <= mandate.begins_at < ends_at
                    or begins_at < mandate.ends_at <= ends_at
                    or mandate.begins_at <= begins_at < ends_at <= mandate.ends_at):
                raise forms.ValidationError("La période définie pour ce mandat empiète sur la période d'un autre "
                                            "mandat.", code='invalidMandate')


class PeopleForm(forms.ModelForm):
    class Meta(object):
        model = People
        fields = ['first_name', 'last_name', 'email', 'phone', 'role']

    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'peopleForm'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'


class RequirementForm(forms.ModelForm):
    active_until = forms.DateTimeField(
        label="Date de fin de validité",
        help_text="Format : JJ/MM/AAAA HH:mm:ss"
    )

    help_text = forms.Field(
        label="Texte d'aide",
        help_text="S'affiche à côté du critère dans la section situation administrative d'une association",
        required=False
    )

    data = forms.Field(
        label="Méta-données",
        initial="{}"
    )

    class Meta(object):
        model = Requirement
        fields = ['name', 'type', 'data', 'help_text', 'active_until']

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'requirementForm'
        self.helper.form_error_title = 'Veuillez corriger les erreurs suivantes :'

    def clean(self):
        super(RequirementForm, self).clean()
        active_until = self.cleaned_data.get('active_until')
        type = self.cleaned_data.get('type')
        data = self.cleaned_data.get('data')

        if not active_until:
            raise forms.ValidationError("La date de fin de validité a un format incorrect ou est manquante.", code='missingActiveUntil')

        # We ensure active_until is strictly before current time
        if active_until.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
            raise forms.ValidationError("La date de fin de validité ne peut pas être dans le passé.",
                                        code='invalidActiveUntil')

        if type in dict(Requirement.REQUIREMENT_TYPES):
            if type == 'file' or type == 'mandate':
                try:
                    data = json.loads(data)
                except Exception:
                    raise forms.ValidationError(
                        "Les méta-données sont invalides, veuillez respecter le format associé au type de critère choisit !",
                        code='invalidDataFormat')
            else:
                if data != "{}":
                    raise forms.ValidationError(
                        "Les méta-données sont invalides, veuillez laisser la valeur {} pour ce type de critère !",
                        code='invalidDataForThisType')

            if type == 'file':
                if 'tag_id' in data:
                    try:
                        folder_id = int(data['tag_id'])
                        folder = FileFolder.objects.filter(id=folder_id).first()
                        if folder is None:
                            raise FileFolder.DoesNotExist
                    except ValueError:
                        raise forms.ValidationError(
                            "L'id du dossier est invalide, il faut un entier !",
                            code='missingDataFolder')
                    except FileFolder.DoesNotExist:
                        raise forms.ValidationError(
                            "Ce dossier n'existe pas, veuillez le créer ou en prendre un autre !",
                            code='invalidDataFolder')
                else:
                    raise forms.ValidationError(
                        "Il manque l'id du dossier dans les méta-données. Le format attendu est {\"tag_id\":\"XX\"} où XX est l'id du dossier.",
                        code='missingDataFolder')
            if type == 'mandate':
                if 'year' in data and len(data['year']) == 4:
                    try:
                        int(data['year'])
                    except ValueError:
                        raise forms.ValidationError(
                            "L'année du mandat est invalide, il faut un entier à 4 chiffres !",
                            code='invalidDataMandate')
                else:
                    raise forms.ValidationError(
                        "Il manque l'année du mandat dans les méta-données. Le format attendu est {\"year\":\"XXXX\"} où XXXX est l'année du mandat.",
                        code='missingDataMandate')
        else:
            raise forms.ValidationError("Ce type de critère n'existe pas, veuillez en sélectionner un dans la liste.",
                                        code='invalidType')
