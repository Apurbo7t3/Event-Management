from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    profile_image=models.ImageField(
        upload_to='profile_image',
        default='profile_image/default_profile.jpg',
        blank=True,null=True,
    )
    phone_number=models.TextField(blank=True)
    bio=models.TextField(blank=True)
