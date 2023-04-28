from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class NewUser(User):
    age = models.PositiveIntegerField(blank=True, null=True)
    is_doctor = models.BooleanField(default=False, blank=True)
    is_patient = models.BooleanField(default=False, blank=True)
    is_nurse = models.BooleanField(default=False, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)


class Doctor(models.Model):
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(
        NewUser, related_name="doctor", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        NewUser, related_name="patient", on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, related_name="patient", blank=True, null=True
    )
    mobile_phone = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    city = models.CharField(max_length=100, default="-", blank=True, null=True)
    state = models.CharField(max_length=100, default="-", blank=True, null=True)
    country = models.CharField(max_length=100, default="-", blank=True, null=True)
    house_address = models.CharField(max_length=500, default="-", blank=True, null=True)
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, null=True, blank=True, related_name="address"
    )

    def __str__(self):
        return (
            self.patient.user.first_name
            + " "
            + self.patient.user.last_name
            + " Address "
        )


class Disease(models.Model):
    name = models.CharField(max_length=100)
    stage = models.CharField(max_length=12)
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="disease"
    )

    def __str__(self):
        return (
            self.patient.user.first_name
            + " "
            + self.patient.user.last_name
            + " has "
            + self.name
        )


class Nurse(models.Model):
    mobile_phone = models.CharField(max_length=12)

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name="nurse")

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    dose = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"


class Prescription(models.Model):
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="prescription"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="prescription"
    )
    medicines = models.ManyToManyField(
        Medicine, related_name="prescriptions", null=True, blank=True
    )

    def __str__(self) -> str:
        return (
            f"{self.doctor.user.first_name} {self.doctor.user.last_name} Prescription"
        )
