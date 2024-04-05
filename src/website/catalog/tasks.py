import os
from celery import shared_task
from django.core.mail import send_mail
from website import settings


@shared_task
def send_join_team_mail(name, contact, speciality, message):
    message_to_send = f'Имя: {name}\nКонтакы: {contact}\nСообщение: {message}'
    send_mail(
        subject=f'Специальность: {speciality}',
        message=message_to_send,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[os.environ['EMAIL_TO']],
        fail_silently=False,
        )
    return "Join team email sent!"
