from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from .models import Appointment

@shared_task
def send_appointment_reminder():
    """Send email reminders for upcoming appointments."""
    tomorrow = timezone.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        appointment_date=tomorrow,
        status__in=['scheduled', 'confirmed']
    ).select_related('patient__user', 'doctor__user')

    for appointment in appointments:
        # Prepare email context
        context = {
            'patient_name': appointment.patient.user.get_full_name(),
            'doctor_name': appointment.doctor.user.get_full_name(),
            'appointment_date': appointment.appointment_date,
            'appointment_time': appointment.time_slot.start_time,
        }

        # Send email to patient
        patient_email = appointment.patient.user.email
        if patient_email:
            send_mail(
                subject='Appointment Reminder',
                message=render_to_string('appointments/email/reminder.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient_email],
                html_message=render_to_string('appointments/email/reminder.html', context)
            )

@shared_task
def send_appointment_confirmation(appointment_id):
    """Send confirmation email when an appointment is scheduled."""
    try:
        appointment = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).get(id=appointment_id)

        context = {
            'patient_name': appointment.patient.user.get_full_name(),
            'doctor_name': appointment.doctor.user.get_full_name(),
            'appointment_date': appointment.appointment_date,
            'appointment_time': appointment.time_slot.start_time,
            'reason': appointment.reason,
        }

        # Send email to patient
        patient_email = appointment.patient.user.email
        if patient_email:
            send_mail(
                subject='Appointment Confirmation',
                message=render_to_string('appointments/email/confirmation.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient_email],
                html_message=render_to_string('appointments/email/confirmation.html', context)
            )

        # Send email to doctor
        doctor_email = appointment.doctor.user.email
        if doctor_email:
            send_mail(
                subject='New Appointment Scheduled',
                message=render_to_string('appointments/email/doctor_notification.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor_email],
                html_message=render_to_string('appointments/email/doctor_notification.html', context)
            )

    except Appointment.DoesNotExist:
        pass

@shared_task
def send_cancellation_notification(appointment_id, cancelled_by_name, reason):
    """Send notification when an appointment is cancelled."""
    try:
        appointment = Appointment.objects.select_related(
            'patient__user', 'doctor__user'
        ).get(id=appointment_id)

        context = {
            'patient_name': appointment.patient.user.get_full_name(),
            'doctor_name': appointment.doctor.user.get_full_name(),
            'appointment_date': appointment.appointment_date,
            'appointment_time': appointment.time_slot.start_time,
            'cancelled_by': cancelled_by_name,
            'reason': reason,
        }

        # Send email to patient
        patient_email = appointment.patient.user.email
        if patient_email:
            send_mail(
                subject='Appointment Cancelled',
                message=render_to_string('appointments/email/cancellation.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient_email],
                html_message=render_to_string('appointments/email/cancellation.html', context)
            )

        # Send email to doctor
        doctor_email = appointment.doctor.user.email
        if doctor_email:
            send_mail(
                subject='Appointment Cancelled',
                message=render_to_string('appointments/email/cancellation.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor_email],
                html_message=render_to_string('appointments/email/cancellation.html', context)
            )

    except Appointment.DoesNotExist:
        pass

@shared_task
def cleanup_expired_appointments():
    """Mark appointments as 'no_show' if they're past due and weren't completed."""
    today = timezone.now().date()
    past_appointments = Appointment.objects.filter(
        appointment_date__lt=today,
        status__in=['scheduled', 'confirmed']
    )

    for appointment in past_appointments:
        appointment.status = 'no_show'
        appointment.save()

        # Notify relevant parties
        context = {
            'patient_name': appointment.patient.user.get_full_name(),
            'doctor_name': appointment.doctor.user.get_full_name(),
            'appointment_date': appointment.appointment_date,
            'appointment_time': appointment.time_slot.start_time,
        }

        # Send email to patient
        patient_email = appointment.patient.user.email
        if patient_email:
            send_mail(
                subject='Missed Appointment Notification',
                message=render_to_string('appointments/email/no_show.txt', context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[patient_email],
                html_message=render_to_string('appointments/email/no_show.html', context)
            ) 