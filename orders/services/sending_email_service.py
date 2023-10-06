from django.conf import settings
from django.core.mail import send_mail


def send_email_to_customer(
        subject: str,
        message: str,
        from_email: str,
        recipient_list: list
) -> None:
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD
    )
