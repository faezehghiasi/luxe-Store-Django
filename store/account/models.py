from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import os

def _get_avatar_upload_path(instance, filename):
    now = timezone.now()
    base_path = 'avatars'
    new_filename = str(uuid.uuid5(uuid.NAMESPACE_URL,instance.id))
    ext = os.path.splitext(filename)[1]
    path = os.path.join(base_path, now.strftime("%Y/%m"), f"{new_filename}{ext}")
    return path


class User(AbstractUser):
    email = models.EmailField("Email Address")
    phoneNumber = models.CharField('Phone Number', max_length=15)
    address = models.TextField('Address')
    #avatar = models.ImageField(upload_to='avatars/%Y/%m', null=True, blank=True)
    avatar = models.ImageField(upload_to=_get_avatar_upload_path, null=True, blank=True)
    def __str__(self):
        return self.username

