from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

def user_directory_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    bio = models.CharField(max_length=300, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)