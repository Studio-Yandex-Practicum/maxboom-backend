from django.core.exceptions import ValidationError


def clean(obj):
    """
    Проверяет модель на предмет уже существующих объектов
    и выкидывает ValidationError в случае, если они уже есть.
    """

    # Проверка осуществляется на уровне создания нового объекта
    # и редактирования существующих, поэтому она позволяет создать
    # новый объект модели при отсутствии других или же
    # валидирует изменения, если у объекта уже есть атрибуты.
    if not obj.__class__.objects.count():
        return obj
    if obj.__class__.objects.count() > 0 and obj.pk is None:
        raise ValidationError(
            f'Может быть только один объект '
            f'"{obj._meta.verbose_name}"!'
        )

