from django.db import models
from django.conf import settings

class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    emergency_contact_relationship = models.CharField(max_length=50)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_gender_display()})"

    def get_age(self):
        if self.user.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.user.date_of_birth.year - (
                (today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day)
            )
        return None

    def get_medical_summary(self):
        return {
            'blood_group': self.blood_group,
            'allergies': self.allergies.split(',') if self.allergies else [],
            'medical_conditions': self.medical_conditions.split(',') if self.medical_conditions else [],
            'current_medications': self.current_medications.split(',') if self.current_medications else [],
        } 