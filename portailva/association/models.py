import json
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from portailva.file.models import AssociationFile
from portailva.utils.fields import LogoURLField
from portailva.utils.models import Place
from portailva.utils.validators import validate_iban, validate_siren


class Category(models.Model):
    """
    A Category is a simple container for Associations.
    There is no kind of logic in a Category. It simply here for Association presentation in a predefined order.
    """
    name = models.CharField("Nom", max_length=50)
    position = models.IntegerField("Position")
    latex_color_name = models.CharField(max_length=100,
                                        help_text="Used for LaTeX generation, see the .sty for more info")

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name

    def get_directory_associations(self):
        return (self.association_set
                .filter(is_validated=True)
                .filter(directory_entries__isnull=False)
                .filter(directory_entries__is_online=True)
                .distinct()
                .order_by('name'))


class Association(models.Model):
    """
    An Association.
    """
    name = models.CharField("Nom officiel", max_length=50)
    acronym = models.CharField("Nom usuel ou acronyme", max_length=20, null=True, blank=True)
    description = models.TextField(
        "Description",
        help_text="Cette description n'est pas visible dans le Bot'INSA",
    )
    active_members_number = models.PositiveIntegerField("Nombre de membres actifs", default=0)
    all_members_number = models.PositiveIntegerField("Nombre de membres adhérents", default=0)

    is_active = models.BooleanField("Est active", default=True)
    is_validated = models.BooleanField("Est validée", default=False)
    has_place = models.BooleanField("Possède un local?", default=False)
    room = models.ForeignKey(Place, verbose_name="Local", related_name="association", blank=True, null=True,
                              on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, verbose_name="Catégorie", on_delete=models.PROTECT)
    users = models.ManyToManyField(User, verbose_name="Utilisateurs", related_name='associations', blank=True)

    commentary = models.TextField(
        "Commentaires",
        help_text="Cette description n'est pas visible pour les non-administateurs",
        blank=True
    )
    moderated_by = models.ManyToManyField(User, verbose_name="Référent CVA", related_name='referent', blank=True)

    logo_url = LogoURLField("URL du logo", blank=True)

    iban = models.CharField("IBAN", max_length=50, blank=True, validators=[validate_iban])
    bic = models.CharField("BIC", max_length=15, blank=True)
    rna = models.CharField("Numéro RNA", max_length=10, blank=True, help_text="La date extacte ainsi que les numéros d'identifications ci-dessous peuvent être facilement retrouvés en cherchant votre asso sur le site : entreprise.data.gouv.fr")
    siren = models.CharField("Numéro SIREN", max_length=9, blank=True, help_text="Format : XXXXXXXXX où X est un chiffre entre 0 et 9", validators=[validate_siren])

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    created_officially_at = models.DateField("Date de création", help_text="Format : JJ/MM/AAAA", null=True, blank=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name

    def current_directory_entry(self):
        return self.directory_entries.filter(is_online=True).last()

    def online_events(self):
        return self.events.filter(is_online=True).filter(ends_at__gte=datetime.now()).order_by('begins_at')

    def can_admin(self, user):
        """
        Checks if an user can administrate an association.
        The association can be administrated if:
        - The user is an admin
        :param user: the user to check the rights
        :return: `True` if the user can access this association, `False` otherwise.
        """
        if user is not None and user.is_authenticated:
            if user.is_superuser or user.has_perm('association.admin_association'):
                return True

        return False

    def can_access(self, user):
        """
        Checks if an user can access information about an association.
        The association can be accessed if:
        - The user belongs to association users list
        - The user is an admin
        :param user: the user to check the rights
        :return: `True` if the user can access this association, `False` otherwise.
        """
        if user is not None and user.is_authenticated:
            if self.can_admin(user):
                return True
            elif user in self.users.all():
                return True

        return False


class Mandate(models.Model):
    """
    A Mandate is an Association period of activity. During a Mandate, some people manage the Association (like the
    president or the treasurer).
    """
    begins_at = models.DateField("Début du mandat")
    ends_at = models.DateField("Fin du mandat")
    share_phone = models.BooleanField("Autoriser le partage du numéro", default=False)
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)

    association = models.ForeignKey(Association, verbose_name="Association", related_name="mandates",
                                    on_delete=models.CASCADE)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return "Du " + str(self.begins_at) + " au " + str(self.ends_at)

    def get_president(self):
        return self.peoples.filter(role__name__istartswith='président')

class PeopleRole(models.Model):
    """
    During a Mandate, each People has a specific PeopleRole.
    """
    name = models.CharField("Nom du poste", max_length=50)
    position = models.IntegerField("Position", blank=True, default=1)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)
        ordering = ('position',)

    def __str__(self):
        return self.name


class People(models.Model):
    """
    A People designates someone who manages the Association during a Mandate.
    """
    first_name = models.CharField("Prénom", max_length=50)
    last_name = models.CharField("Nom", max_length=50)
    email = models.EmailField("Adresse email", max_length=250)
    phone = models.CharField("Numéro de téléphone", max_length=50, default='')

    role = models.ForeignKey(PeopleRole, verbose_name="Rôle", related_name="peoples", on_delete=models.SET_NULL,
                             null=True)
    mandate = models.ForeignKey(Mandate, verbose_name="Mandat", related_name="peoples", on_delete=models.CASCADE)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)
        ordering = ('role',)

    def __str__(self):
        return self.first_name + " " + self.last_name.upper()


class RequirementManager(models.Manager):
    def get_all_active(self):
        return self.all().filter(active_until__gt=datetime.now())


class Requirement(models.Model):
    """
    A Requirement represents an action that an Association can accomplish.
    """
    REQUIREMENT_TYPES = (
        ('mandate', 'Mandat'),
        ('file', 'Fichier'),
        ('accomplishment', 'Validation manuelle'),
        ('room', 'Validation manuelle (nécessite un local)')
    )
    name = models.CharField("Nom", max_length=100)
    type = models.CharField("Type de condition", max_length=40, choices=REQUIREMENT_TYPES)
    data = models.TextField("Meta données", blank=True, default='{}')
    help_text = models.TextField("Texte d'aide", blank=True, null=True)

    active_until = models.DateTimeField("Date de fin de validité")

    objects = RequirementManager()

    class Meta(object):
        ordering = ('name',)
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return '[' + self.type + '] ' + self.name

    def is_achieved(self, association_id):
        data = json.loads(self.data)
        achieved = False
        if self.type == 'file':
            folder_id = int(data['tag_id'])
            nb_files = AssociationFile.objects \
                .filter(association__id=association_id) \
                .filter(folder__id__exact=folder_id) \
                .count()
            if nb_files > 0:
                achieved = True

        if self.type == 'mandate':
            year = data['year']
            try:
                last_mandate = Mandate.objects \
                                   .filter(association__id=association_id) \
                                   .filter(ends_at__year=int(year)) \
                                   .order_by('-ends_at')[0:1].get()
                if last_mandate is not None:
                    people = People.objects.filter(mandate__id=last_mandate.id).count()
                    #President and treasurer at least
                    if people >= 2:
                        achieved = True
            except Mandate.DoesNotExist:
                pass

        if self.type == 'accomplishment':
            accomplishment = Accomplishment.objects \
                .filter(requirement__id=self.id) \
                .filter(association__id=association_id) \
                .count()
            if accomplishment > 0:
                achieved = True

        if self.type == 'room':
            accomplishment = Accomplishment.objects \
                .filter(requirement__id=self.id) \
                .filter(association__id=association_id) \
                .filter(association__has_place=True) \
                .count()
            if accomplishment > 0:
                achieved = True
        return achieved

    def get_folder_id(self):
        data = json.loads(self.data)
        folder_id = int(data['tag_id'])
        return folder_id


class Accomplishment(models.Model):
    """
    An Accomplishment is used to achieve a Requirement manually.
    """
    association = models.ForeignKey(Association, verbose_name="Association", on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, verbose_name="Condition",
                                    limit_choices_to={'type': ['accomplishment', 'room']},
                                    on_delete=models.CASCADE)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin', 'achieve',)

    def __str__(self):
        return '[' + self.association.name + '] ' + self.requirement.name
