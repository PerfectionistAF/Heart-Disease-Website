from django.contrib import admin

from .models import User, Patient, DoctorPatientFile

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(DoctorPatientFile)