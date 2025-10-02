from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Profiles'
        verbose_name = 'Profile'

