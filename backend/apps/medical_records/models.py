from django.db import models
from django.conf import settings

class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('diagnosis', 'Diagnosis'),
        ('treatment', 'Treatment'),
        ('lab_result', 'Laboratory Result'),
        ('prescription', 'Prescription'),
        ('surgery', 'Surgery'),
        ('vaccination', 'Vaccination'),
        ('allergy', 'Allergy'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    record_date = models.DateTimeField()
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to='medical_records/', null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                 null=True, related_name='created_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date']
        permissions = [
            ('view_confidential_records', 'Can view confidential medical records'),
        ]

    def __str__(self):
        return f"{self.patient} - {self.record_type} on {self.record_date}"

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"

class LabResult(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=200)
    test_date = models.DateTimeField()
    result_value = models.CharField(max_length=200)
    normal_range = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    report_file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_name} - {self.test_date}"

class Vaccination(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=200)
    dose_number = models.PositiveIntegerField()
    date_administered = models.DateTimeField()
    administered_by = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100)
    next_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vaccine_name} - Dose {self.dose_number}" 