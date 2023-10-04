from django.core.exceptions import ValidationError


def validate_field_is_string(data: dict, fields_to_validate: list) -> None:
    """Валидация полей, которые должны быть строками.
    Если у модели есть необязательные поля, которые должны быть строками,
    они также могут здесь проверяться.
    """

    for field_to_validate in fields_to_validate:
        if field_to_validate not in data:
            continue
        field = data.get(field_to_validate)
        if field is None or not isinstance(field, str):
            raise ValidationError(
                {f'{field_to_validate}': 'field must be string.'})
