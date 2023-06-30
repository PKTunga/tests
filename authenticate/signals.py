from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from authenticate.models import LoggedInUser
from referrals.models import ReferralRelationship

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
    
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import CustomUser
import uuid

@receiver(post_save, sender=CustomUser)
def update_snapshot_on_save(sender, instance, created, **kwargs):
    if created:
        referral = ReferralRelationship.objects.filter(invited=instance)
        if referral.count() > 0:
            instance.my_inviter = referral[0].inviter
            instance.save()
            
        if instance.is_normal:
            pass
        else:
            instance.is_superuser = True
        instance.save()
