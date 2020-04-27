from django.db.models import URLField
from . import forms

from portailva.utils.validators import validate_image_url, validate_affichage_url


class ImageURLField(URLField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [validate_image_url]
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.ImageURLField,
        }
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)


class LogoURLField(ImageURLField):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = ("Privilégiez les liens en HTTPS. "
                               "Assurez-vous que le lien que vous fournissez "
                               "pointe directement sur l'image (pas de page "
                               "d'affichage comme Google Drive ou autres) et que "
                               "l'image soit accessible. Vous pouvez mettre en ligne votre logo "
                               "dans vos fichiers sur PortailVA, rendre le fichier public et utiliser "
                               "le lien ainsi généré dans ce champ.")
        super().__init__(*args, **kwargs)


class AffichageURLField(URLField):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = ("Privilégiez les liens en HTTPS. "
                               "Assurez-vous que le lien que vous fournissez "
                               "pointe directement sur la ressource (pas de page "
                               "d'affichage comme Google Drive, pas de raccoursiseur de lien ou autres) et que "
                               "la ressource soit accessible. Vous pouvez mettre en ligne une image "
                               "(en .png, .jpg, ou .jpeg, et idéalement au format 1920x1080px), un pdf,"
                               " une vidéo Youtube ou une page web de votre choix.")
        kwargs['validators'] = [validate_affichage_url]
        super().__init__(*args, **kwargs)
