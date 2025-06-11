from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

class EmailService:
    @staticmethod
    def send_email(subject, template_name, context, recipient_list, from_email='italosnobre.si@gmail.com'):
        message = render_to_string(template_name, context)
        if not settings.DEBUG:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
                html_message=message,
            )

    @staticmethod
    def send_reset_password_email(user, token, request):
        reset_password_url = f"{config('DOMAIN')}/redefinir-senha/{token}/"

        EmailService.send_email(
            'Recuperação de Senha',
            'auth/reset_password_email.html',
            {'reset_password_url': reset_password_url},
            [user.email]
        )
        