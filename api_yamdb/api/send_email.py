from django.core.mail import send_mail
from api_yamdb import settings
from django.contrib.auth.tokens import default_token_generator


def send_email(user):
    them = 'Ваш код подтверждения'
    code = default_token_generator.make_token(user)
    text = f'Ваш код подверждения {code}'
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, user.email)


    
