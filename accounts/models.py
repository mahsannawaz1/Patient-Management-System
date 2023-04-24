from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class NewUser(User):

    age = models.PositiveIntegerField(blank=True)
    is_doctor = models.BooleanField(default=False, blank=True)
    is_patient = models.BooleanField(default=False, blank=True)
    is_nurse = models.BooleanField(default=False, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)


class Doctor(models.Model):
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(
        NewUser, related_name="doctor", on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username
