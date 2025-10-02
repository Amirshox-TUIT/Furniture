from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings

from apps.users.tokens import email_verification_token
from django.template.loader import render_to_string


def send_email_confirmation(user, request):
    token = email_verification_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = request.build_absolute_uri(
        reverse('confirmation', kwargs={'uidb64': uidb64, 'token': token})
    )

    subject = "Confirm Your Email Address"
    html_message = render_to_string('users/email_confirmation.html', {
        'user': user,
        'confirmation_link': confirmation_link,
    })

    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)