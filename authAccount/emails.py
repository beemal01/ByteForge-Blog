from django.core.mail import send_mail
from django.conf import settings

class verifyopt:
    def __init__(self, user):
        self.user = user

    def send(self):
        subject = "Verify Email"
        message = f'''
        Dear {self.user.name},
        Your OTP verification code is: {self.user.otp}

        Please enter this code in the verification page to activate your account.
        Note: This code will expire in 10 minutes.

        Regards,
        Bimal Kandel
        '''
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [self.user.email], fail_silently=False)

def verifyopt_send(user):
    verifyopt(user).send()

