from django.db import models
from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string
# Create your models here.

class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    def __unicode__(self):
       return str(self.stripe_id)

class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.confirmed)

    def active_user_email(self):
        """
        send email here & render a string
        """
        activation_url = 'http://localhost:8000/accounts/activation/%s' % (self.activation_key)
        context = {
            'activation_key': self.activation_key,
            'activation_url': activation_url,
            'user': self.user.username,
        }
        subject = 'Activate your email'
        message = render_to_string('accounts/activation_message.txt', context)
        print message
        # self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, *kwargs):
        send_mail(subject, message, from_email, [self.user.email], **kwargs)
