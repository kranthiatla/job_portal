from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(email, username):
    subject = 'Welcome to Job Portal'
    message = f'Hi {username}, thank you for registering!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    return send_mail(subject, message, from_email, recipient_list)
