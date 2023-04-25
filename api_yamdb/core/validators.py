import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    invalid_characters = re.sub(settings.REG_PATTERN, '', value)
    if invalid_characters:
        raise ValidationError(
            f'Недопустимые символы: {invalid_characters}')
    if value == 'me':
        raise ValidationError(
            'Имя пользователя не может быть <me>.',
            params={'value': value},
        )
    return value


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
    return value
