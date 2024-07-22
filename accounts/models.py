from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


    

class CustomUser(AbstractUser):
    username_field = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_not_blocked = models.BooleanField(default=True)
    favorite_stores = models.ManyToManyField('delivery.Store', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '{:06d}'.format(random.randint(0, 999999))
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.is_active and (timezone.now() - self.created_at).seconds < 300