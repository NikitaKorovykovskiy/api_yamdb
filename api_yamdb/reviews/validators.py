from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < 1900 or value > datetime.now().year:
        raise ValidationError('Не верно указан год!')
