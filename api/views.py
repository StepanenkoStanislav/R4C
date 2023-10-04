from http import HTTPStatus

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from api.decorators import exceptions_to_http
from api.utils import get_model_object, get_serial, json_to_dict
from api.validators import validate_field_is_string
from robots.models import Robot


@csrf_exempt
@require_POST
@exceptions_to_http
def add_robot(request):
    data = json_to_dict(request.body)
    validate_field_is_string(data, ['model', 'version', 'created'])
    robot = get_model_object(Robot, data)
    robot.serial = get_serial()
    robot.full_clean()
    robot.save()
    return JsonResponse(
        model_to_dict(robot, exclude='id'), status=HTTPStatus.CREATED)
