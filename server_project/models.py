from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Django Users extention
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#extending-the-existing-user-model

#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #objects_models = models.CharField(max_length=100)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>_<username>/<filename>
    return 'user_{0}_{1}/{2}'.format(instance.user.id, instance.user.username, filename)

class User_File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    modelo = models.FileField(upload_to=user_directory_path)
    size = models.BigIntegerField()
    updated = models.DateField(auto_now_add=True)


# This funtions update or create a Profile model a User is created or modified
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()
