from django.db import models
from django.conf import settings

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specializations = models.ManyToManyField(Specialization)
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=100)  # Stored as comma-separated days
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    max_appointments_per_day = models.PositiveIntegerField(default=20)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {', '.join(s.name for s in self.specializations.all())}"

    def get_available_days_list(self):
        return [day.strip() for day in self.available_days.split(',')]

    def is_available_on_day(self, day):
        return day in self.get_available_days_list()

    def get_appointments_for_date(self, date):
        return self.appointments.filter(appointment_date=date)

    def has_availability_for_date(self, date):
        appointments_count = self.get_appointments_for_date(date).count()
        return appointments_count < self.max_appointments_per_day 