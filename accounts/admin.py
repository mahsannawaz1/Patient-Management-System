from django.contrib import admin
from .models import NewUser, Doctor, Patient, Disease
# Register your models here.
admin.site.register(NewUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Disease)
