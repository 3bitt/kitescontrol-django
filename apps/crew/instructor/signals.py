from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .models import Instructor


# Send signal before Instructor is deleted to delete related User
@receiver(pre_delete, sender=Instructor)
def pre_delete_user(sender, instance, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()