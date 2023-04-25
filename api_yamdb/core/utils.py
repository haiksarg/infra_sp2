from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


SUBJECT = 'YaMDb: код подверждения'
MESSAGE = 'Код подтверждения - {}'


def send_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        SUBJECT,
        MESSAGE.format(confirmation_code),
        settings.EMAIL_HOST_USER,
        [user.email],
    )
