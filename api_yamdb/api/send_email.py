from django.core.mail import send_mail
from api_yamdb.api_yamdb import settings
import random
from api_yamdb.reviews.models import User


def send_email(email):
    them = 'Ваш код подтверждения'
    code = random.randint(1000, 9999)
    text = f'Ваш код подверждения {code}'
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, email)
    user_obj = User.objects.get(emale=email)
    user_obj.code = code
    user_obj.save()
