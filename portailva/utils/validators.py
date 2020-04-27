import re

import requests
from django.core.exceptions import ValidationError

def validate_image_url(url):
    res = requests.head(url, allow_redirects=True)
    if 'image' not in res.headers.get('Content-Type'):
        raise ValidationError("L'URL saisie ne semble pas pointer vers une image valide. "
                              "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
                              "type Google Drive mais bien vers le fichier en lui-même. "
                              "Assurez-vous également que l'accès à l'image ne requière pas "
                              "d'authentification (mode \"public\" sur PortailVA). Vous pouvez mettre en ligne votre "
                              "logo dans vos fichiers sur PortailVA, rendre le fichier public et utiliser "
                              "le lien ainsi généré dans ce champ.")


def validate_affichage_url(url):
    res = requests.head(url, allow_redirects=False)
    if res.status_code in [400, 401, 402, 403, 404, 500, 501, 502, 503]:
        raise ValidationError("L'URL saisie ne semble pas pointer vers une ressource valide. "
                              "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une ressource indisponible"
                              " publiquement et que cette dernière existe bien.")
    if res.is_redirect or res.is_permanent_redirect:
        raise ValidationError("L'URL saisie ne semble pas pointer vers une ressource valide. "
                              "Assurez-vous que l'URL que vous fournissez ne pointe pas vers une visionneuse "
                              "type Google Drive, mais bien vers le fichier en lui-même. "
                              "Vérifiez que votre URL ne correspond pas à un raccoursiseur de lien "
                              "(les redirections ne sont pas autorisés).")


def validate_iban(iban):
    fr_iban_re = re.compile(r'^FR[0-9A-Z]{25}$')
    if not fr_iban_re.match(iban):
        raise ValidationError("L'IBAN saisi n'est pas valide. "
                              "Il doit commencer par FR et ne contenir que "
                              "des lettres majuscules ou des chiffres (pas d'espace, de tirets, ...). "
                              "27 caractères au total.")

    verif_iban = list(iban[4:] + iban[:4])
    verif_iban_num = ''
    for c in verif_iban:
        if 'A' <= c <= 'Z':
            c = str(ord(c) - ord('A') + 10)
        verif_iban_num += c
    verif_iban_num = int(verif_iban_num)

    if verif_iban_num % 97 != 1:
        raise ValidationError("L'IBAN saisi a la bonne forme mais n'est pas valide.")


def validate_siren(siren):
    _digits_re = re.compile(r'^[0-9]+$')
    if not bool(_digits_re.match(siren)) or not bool(siren) or len(siren) < 9:
        raise ValidationError("Le numéro SIREN saisi a un format invalide. "
                              "Il doit contenir que des chiffres (pas d'espace, de tirets ...). "
                              "9 chiffres au total.")
    sum = 0
    for i in range(len(siren)):
        if (i % 2) == 1:
            num_tmp = int(siren[i], 10) * 2
            if num_tmp > 9:
                num_tmp -= 9
        else:
            num_tmp = int(siren[i], 10)
        sum += num_tmp

    is_valid = bool((sum % 10) == 0)
    if not is_valid:
        raise ValidationError("Le numéro SIREN saisi est invalide. "
                              "La vérification du dernier chiffre de validation a échoué.")

