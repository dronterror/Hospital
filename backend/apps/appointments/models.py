from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

class TimeSlot(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.doctor} - {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    reason = models.TextField()
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    cancelled_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, 
                                   on_delete=models.SET_NULL, related_name='cancelled_appointments')
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', 'time_slot__start_time']
        unique_together = ['doctor', 'appointment_date', 'time_slot']

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date} at {self.time_slot.start_time}"

    def clean(self):
        if self.appointment_date and self.appointment_date < timezone.now().date():
            raise ValidationError("Cannot schedule appointments in the past.")
        
        if not self.doctor.is_available_on_day(self.appointment_date.strftime('%A')):
            raise ValidationError(f"Doctor is not available on {self.appointment_date.strftime('%A')}s")
        
        if not self.doctor.has_availability_for_date(self.appointment_date):
            raise ValidationError("Doctor has reached maximum appointments for this date.")
        
        # Check if the time slot belongs to the doctor
        if self.time_slot and self.time_slot.doctor != self.doctor:
            raise ValidationError("Invalid time slot for this doctor.")
        
        # Check if the time slot is available
        if self.time_slot and not self.time_slot.is_available:
            raise ValidationError("This time slot is not available.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:  # New appointment
            self.time_slot.is_available = False
            self.time_slot.save()
        super().save(*args, **kwargs)

    def cancel(self, cancelled_by, reason):
        """Cancel an appointment with proper logging and notification."""
        if self.status == 'completed':
            raise ValidationError("Cannot cancel a completed appointment.")
        
        self.status = 'cancelled'
        self.cancelled_by = cancelled_by
        self.cancellation_reason = reason
        self.time_slot.is_available = True
        self.time_slot.save()
        self.save()

    def complete(self, notes=None, prescription=None, follow_up_date=None):
        """Mark an appointment as completed with optional follow-up."""
        if self.status not in ['confirmed', 'in_progress']:
            raise ValidationError("Only confirmed or in-progress appointments can be completed.")
        
        self.status = 'completed'
        if notes:
            self.notes = notes
        if prescription:
            self.prescription = prescription
        if follow_up_date:
            self.follow_up_date = follow_up_date
        self.save()

    def reschedule(self, new_date, new_time_slot):
        """Reschedule an appointment to a new date and time."""
        if self.status in ['completed', 'cancelled']:
            raise ValidationError("Cannot reschedule completed or cancelled appointments.")
        
        old_time_slot = self.time_slot
        self.appointment_date = new_date
        self.time_slot = new_time_slot
        
        # Make the old time slot available
        old_time_slot.is_available = True
        old_time_slot.save()
        
        # Mark the new time slot as unavailable
        new_time_slot.is_available = False
        new_time_slot.save()
        
        self.save() 