from django.contrib import admin
from .models import (
    NewUser,
    Doctor,
    Patient,
    Disease,
    Nurse,
    Admin,
    Medicine,
    Prescription,
    Address,
)

# Register your models here.
admin.site.register(NewUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Address)
admin.site.register(Disease)
admin.site.register(Nurse)
admin.site.register(Admin)
admin.site.register(Medicine)
admin.site.register(Prescription)
