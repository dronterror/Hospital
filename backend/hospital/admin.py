from django.contrib import admin
from .models import Doctor, Appointment, DoctorSchedule

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
