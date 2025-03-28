from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField("Email Address")
    phoneNumber = models.CharField('Phone Number', max_length=15)
    address = models.TextField('Address')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return self.username

