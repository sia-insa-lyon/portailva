from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime

from portailva.association.models import Association
from portailva.file.models import File
from portailva.utils.fields import LogoURLField, AffichageURLField
from portailva.utils.models import Place


class EventType(models.Model):
    name = models.CharField("Nom", max_length=50)
    color = models.CharField("Couleur", max_length=7, default="#007bff")

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name


class EventManager(models.Manager):
    def get_online(self):
        return self.all().filter(is_online=True)


class Event(models.Model):
    name = models.CharField("Nom", max_length=50)
    short_description = models.TextField("Description courte", max_length=150)
    description = models.TextField("Description")

    is_online = models.BooleanField("Est publié", default=False)

    type = models.ForeignKey(EventType, verbose_name="Type d'événement", related_name="events", null=True,
                             on_delete=models.SET_NULL)
    association = models.ForeignKey(Association, verbose_name="Association", related_name="events",
                                    on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name="Lieu", related_name="events", blank=True, null=True,
                              on_delete=models.SET_NULL)
    logo_url = LogoURLField("URL du logo", blank=True)

    begins_at = models.DateTimeField("Date et heure de début")
    ends_at = models.DateTimeField("Date et heure de fin")
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    website_url = models.URLField("Page web", blank=True)
    facebook_url = models.URLField("Evènement Facebook", blank=True)

    # Affichage stuff
    has_poster = models.BooleanField("Est à publier sur Affichage ?", default=False)
    begin_publication_at = models.DateTimeField(verbose_name="Début d'affichage", blank=True, null=True)
    end_publication_at = models.DateTimeField(verbose_name="Fin d'affichage", blank=True, null=True)
    content_url = AffichageURLField(verbose_name='Url du contenu', blank=True, null=True)
    duration = models.IntegerField(verbose_name="Durée d'apparition à l'écran (en s)", blank=True, default=7)

    objects = EventManager()

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return "{} - {}".format(self.name, self.begins_at.strftime('%d/%m/%Y'))

    def can_update(self, user):
        if not user.has_perm('event.admin_event'):
            if not user in self.association.users.all():
                return False
            # Forbid non-admin user to change events which are already started or finished
            elif self.begins_at.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                return False
            else:
                return True
        else:
            return True

    def can_delete(self, user):
        if not user.has_perm('event.admin_event'):
            if not user in self.association.users.all():
                return False
            elif self.is_online and self.ends_at.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
                return False
            else:
                return True
        else:
            return True


class EventPrice(models.Model):
    name = models.CharField("Nom du tarif", max_length=50)
    price = models.DecimalField("Tarif", max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0'))])

    event = models.ForeignKey(Event, verbose_name="Evénement", related_name="prices", on_delete=models.CASCADE)

    is_va = models.BooleanField("Est un tarif VA ?", default=False)
    is_variable = models.BooleanField("Prix libre ?", default=False)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return '[' + self.event.name + '] ' + self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # We delete price value if price is variable
        if self.is_variable:
            self.price = 0.0
        return super(EventPrice, self).save(force_insert, force_update, using, update_fields)
