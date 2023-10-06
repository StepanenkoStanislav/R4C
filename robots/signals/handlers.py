from typing import Type

from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.services import (
    TEMPLATE_MESSAGE_ABOUT_ROBOT_ARRIVAL,
    TEMPLATE_SUBJECT_ABOUT_ROBOT_ARRIVAL
)
from orders.services.sending_email_service import send_email_to_customer
from robots.models import Robot


@receiver(post_save, sender=Robot)
def print_email(sender: Type[ModelBase], instance: Robot, **kwargs) -> None:
    if kwargs.get('created'):
        return
    order = Order.objects.filter(robot_serial=instance.serial).first()
    if not order:
        return
    send_email_to_customer(
        TEMPLATE_SUBJECT_ABOUT_ROBOT_ARRIVAL.format(
            model=instance.model,
            version=instance.version
        ),
        TEMPLATE_MESSAGE_ABOUT_ROBOT_ARRIVAL.format(
            model=instance.model,
            version=instance.version
        ),
        settings.EMAIL_HOST_USER,
        [order.customer.email],
    )
