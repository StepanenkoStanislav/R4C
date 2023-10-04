import re
from string import ascii_letters, digits
from typing import TypeVar

from django.db.models import Model

from robots.models import Robot

FIELD_NAME_PATTERN = re.compile(r"(?P<field>'.+')")

SERIAL_LENGTH = Robot._meta.get_field('serial').max_length

LETTERS_AND_DIGITS = ascii_letters + digits

DjangoModel = TypeVar('DjangoModel', bound=Model)
