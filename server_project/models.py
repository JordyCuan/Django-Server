from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Django Users extention
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-the-existing-user-model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #objects_models = models.CharField(max_length=100)

class Objects_Models(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    originalname = models.TextField(unique=True)
    localname = models.TextField()
    path_and_name = models.TextField()
    path = models.TextField()
    encoding = models.TextField()
    mimetype = models.TextField()
    size = models.BigIntegerField()
    updated = models.DateField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()