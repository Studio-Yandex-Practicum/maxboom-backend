from django.core.exceptions import ValidationError


def clean(obj):
    """
    Проверяет модель на предмет уже существующих объектов
    и выкидывает ValidationError в случае, если они уже есть.
    """

    if obj.__class__.objects.count() > 0:
        raise ValidationError(
            f'Может быть только один объект '
            f'"{obj._meta.verbose_name}"!'
        )

