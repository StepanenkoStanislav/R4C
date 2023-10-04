from functools import wraps
from http import HTTPStatus

from django.core.exceptions import BadRequest, ValidationError
from django.http import JsonResponse


def exceptions_to_http(view_func):
    """Преобразовывает ошибки при валидации запроса в JsonResponse."""

    @wraps(view_func)
    def inner(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except BadRequest as err:
            return JsonResponse(*err.args, status=HTTPStatus.BAD_REQUEST)
        except ValidationError as err:
            return JsonResponse(
                err.message_dict, status=HTTPStatus.BAD_REQUEST)
    return inner
