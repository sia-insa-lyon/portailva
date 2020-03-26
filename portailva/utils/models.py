from django.db import models


# Create your models here.
class Place(models.Model):
    """
    A Place somewhere.
    """
    name = models.CharField("Nom", max_length=50)
    lat = models.DecimalField("Latitude", max_digits=8, decimal_places=6)
    long = models.DecimalField("Longitude", max_digits=8, decimal_places=6)
    is_room = models.BooleanField("Est un local", default=False)

    class Meta(object):
        default_permissions = ('add', 'change', 'delete', 'admin',)

    def __str__(self):
        return self.name
