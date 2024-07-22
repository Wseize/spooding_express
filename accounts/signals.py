# otp_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import send_otp_sms

@receiver(post_save, sender=UserProfile)
def send_otp_on_new_number(sender, instance, created, **kwargs):
    if created:
        send_otp_sms(instance.phone_number)
