from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


# celery task function
@shared_task
def send_welcome_email(user_email, user_username):
    subject = 'User has registered successfully. '
    message = f'Welcome to our platform {user_username}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

# send email function to send mail
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
