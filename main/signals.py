from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import SellerTemplates, Templates

from .models import VPS


# @receiver(post_save, sender=SellerTemplates)
# def update_snapshot_on_save(sender, instance, created, **kwargs):
#     print("ignalssssssssssssssssssssssss")
#     print(instance._old_cost)
#     print(instance.cost)
#     print(instance._old_quantity)
#     print(instance.quantity)
#     if instance._old_cost  != instance.cost or instance._old_quantity != instance.quantity:
#         old = instance._old_cost * instance._old_quantity
#         new = instance.cost * instance.quantity
#         instance.total_cost = instance.total_cost - old
#         instance.total_cost = instance.total_cost + new
#         instance.save()
        
#     if instance._old_quantity != instance.quantity:
#         template = instance.template
#         old = template.cost * instance._old_quantity
#         new = template.cost * instance.quantity
#         template.total_cost = template.total_cost - old
#         template.total_cost = template.total_cost + new
#         template.save()
        
        
        
import uuid
@receiver(post_save, sender=VPS)
def update_snapshot_on_save(sender, instance, created, **kwargs):
    if created:
        if instance.template.generation == "auto":
            pass
        else:
            instance.instance_id = str(uuid.uuid4().hex)
            instance.save()
