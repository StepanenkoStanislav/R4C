import json
import random
import re
from typing import Type

from django.core.exceptions import BadRequest, ValidationError

from api import (
    FIELD_NAME_PATTERN, LETTERS_AND_DIGITS, ROBOT_SERIAL_LENGTH, DjangoModel)


def json_to_dict(data: [str, bytes, bytearray]) -> dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise BadRequest({'error': ['JSON is not valid.']})


def get_model_object(model: Type[DjangoModel], data: dict) -> DjangoModel:
    try:
        return model(**data)
    except TypeError as err:
        field = re.search(FIELD_NAME_PATTERN, *err.args).group('field')
        raise ValidationError({'error': f'name {field} is not correct.'})


def get_serial() -> str:
    return ''.join(
        [random.choice(LETTERS_AND_DIGITS) for _ in range(
            ROBOT_SERIAL_LENGTH)])
