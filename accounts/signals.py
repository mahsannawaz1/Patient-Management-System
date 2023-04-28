from django.db.models.signals import post_save
from .models import Patient, Address
from django.dispatch import receiver


@receiver(post_save, sender=Patient)
def create_address(sender, instance, created, **kwargs):
    if created:
        address = Address.objects.create(patient=instance)
        address.save()
