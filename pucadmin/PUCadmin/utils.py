from typing import Union, List

from django.conf import settings
from django.core import mail
from django.template import loader


def send_email(
    to: Union[str, List[str]], subject: str, body_template: str, context: dict
) -> None:
    receivers = [to] if type(to) is str else to
    mail.EmailMessage(
        subject,
        loader.render_to_string(body_template, context),
        settings.DEFAULT_FROM_EMAIL,
        receivers,
    ).send()
