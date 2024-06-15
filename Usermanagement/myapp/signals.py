from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group

@receiver(post_save, sender=User)
def create_user_profile(sender,created,instance,**kwargs):
    if created:
        user=instance
        group=Group.objects.get(name="default")
        user.groups.add(group)