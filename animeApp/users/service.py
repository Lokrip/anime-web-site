from django.core.mail import send_mail
from animeApp.settings import EMAIL_HOST_USER

def send(user_email, activation_link):
    send_mail(
        "Подтверждение регистрации",
        f'Для активации аккаунта перейдите по ссылке: {activation_link}',
        EMAIL_HOST_USER,
        [user_email],
    )