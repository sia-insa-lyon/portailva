import uuid

from django.conf import settings
from django.db import models
from django.dispatch import receiver


class FileType(models.Model):
    """
    A FileType defines characteristics of a file (extension, MIME type, etc.).
    """
    name = models.CharField("Nom", max_length=50)
    mime_type = models.CharField("Type MIME", max_length=100)

    def __str__(self):
        return self.name


class File(models.Model):
    """
    A File.
    """
    uuid = models.UUIDField("uuid", default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("Nom", max_length=200)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name

    def can_access(self, user):
        if hasattr(self, 'resourcefile') and self.resourcefile.is_public:
            return True
        if isinstance(self, AssociationFile) and self.folder.is_public:
            return True
        if hasattr(self, 'associationfile') and self.associationfile.folder.is_public:
            return True
        # By default, user must be logged in
        if user is not None and user.is_authenticated:
            # If file is an association file, we ensure user belongs to association or is an admin
            if isinstance(self, AssociationFile):
                return self.association.can_access(user)
            elif hasattr(self, 'associationfile'):
                return self.associationfile.association.can_access(user)
            else:
                return True
        return False


class TreeObject(models.Model):

    class Meta:
        abstract = True

    parent = models.ForeignKey('self', verbose_name="Dossier parent", related_name='children', null=True, blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField("Nom", max_length=250)

    def get_tree(self):
        tree = []
        if self.parent is not None:
            tree.extend(self.parent.get_tree())
        tree.append(self.name)
        return tree

    def get_path(self):
        tree = self.get_tree()
        return '/'.join(tree)

    @property
    def tree(self):
        return self.get_tree()

    @property
    def path(self):
        return self.get_path()

    def __str__(self):
        return self.name


class FileFolder(TreeObject):
    """
    A File Folder is used for Association File sorting.
    """
    description = models.TextField("Description")
    position = models.IntegerField("Position", blank=True)
    is_writable = models.BooleanField("Accessible en écriture ?", default=True)

    is_public = models.BooleanField("Public", default=False, blank=True)

    allowed_types = models.ManyToManyField(FileType, verbose_name="Extensions autorisées", blank=True)

    def __str__(self):
        return self.name

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in FileFolder.objects.filter(parent=self):
            r.append(c.get_all_children(include_self=False))


class AssociationFile(File):
    association = models.ForeignKey('association.Association', related_name="files", verbose_name="Association", null=True,
                                    blank=True, on_delete=models.CASCADE)
    folder = models.ForeignKey(FileFolder, verbose_name="Dossier", related_name="files", on_delete=models.CASCADE)


class ResourceFolder(TreeObject):
    """
    Resource folder to store ResourceFile objects.
    """

    def list(self):
        """ List resources into this directory """
        sub_folders = self.children.all()
        resources = self.resources.all()
        return sub_folders + resources

    @staticmethod
    def all_by_tree(folder=None, folders_list=None):
        """
        List all tree of resource folders.
        This fetch mode is useful for administration sections
        :type folders_list: list
        :param folders_list: List of previously added folders
        :type folder: ResourceFolder
        """
        if folders_list is None:
            folders_list = []
        if folder is None:
            folders = ResourceFolder.objects.filter(parent=None).all()
        else:
            folders = folder.children.all()
        for folder in folders:
            folders_list.append(folder)
            ResourceFolder.all_by_tree(folder, folders_list)
        return folders_list


class ResourceFile(File):
    class Meta:
        permissions = (
            ("file.manage_resources", "Gérer les resources disponibles aux associations"),
        )

    published = models.BooleanField('Publié', default=False)
    folder = models.ForeignKey(ResourceFolder, verbose_name="Dossier", default=None, blank=True,
                               related_name="resources", null=True, on_delete=models.CASCADE)
    is_public = models.BooleanField("Public", default=False, blank=True)

    def can_access(self, user):
        if (user is not None and user.is_authenticated) or self.is_public:
            return self.published
        return False


# noinspection PyUnusedLocal
def user_directory_path(instance, filename):
    return 'uploads/' + str(uuid.uuid1())


class FileVersion(models.Model):
    """
    A specific File Version.
    """
    version = models.IntegerField("Numéro de version")
    data = models.FileField(upload_to=user_directory_path, verbose_name="Version")

    file = models.ForeignKey(File, verbose_name="Fichier", related_name="versions", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Utilisateur", null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière mise à jour", auto_now=True)

    def __str__(self):
        return '#{} - {} (V{})'.format(self.pk, self.file.name, self.version)


# noinspection PyUnusedLocal
@receiver(models.signals.pre_delete, sender=FileVersion)
def file_version_delete(sender, instance, **kwargs):
    instance.data.delete(False)
