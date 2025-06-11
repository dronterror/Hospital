from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.db.models.functions import TruncDate


@shared_task
def send_appointment_confirmation_email(appointment_id):
    from .models import Appointment

    try:
        appointment = Appointment.objects.get(id=appointment_id)

        subject = f'Appointment Confirmation: {appointment.date_time.strftime("%Y-%m-%d %H:%M")}'
        message = f'''
        Dear {appointment.patient.user.get_full_name()},

        Your appointment with Dr. {appointment.doctor.user.get_full_name()} has been confirmed for {appointment.date_time.strftime("%Y-%m-%d at %H:%M")}.

        Please arrive 15 minutes before your scheduled appointment.

        Thank you,
        Hospital Team
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email='hospital@example.com',
            recipient_list=[appointment.patient.user.email],
            fail_silently=False,
        )

        return f"Confirmation email sent to {appointment.patient.user.email}"
    except Appointment.DoesNotExist:
        return f"Appointment with id {appointment_id} does not exist"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def send_appointment_reminder_email(appointment_id):
    from .models import Appointment

    try:
        appointment = Appointment.objects.get(id=appointment_id)

        subject = f'Appointment Reminder: {appointment.date_time.strftime("%Y-%m-%d %H:%M")}'
        message = f'''
        Dear {appointment.patient.user.get_full_name()},

        This is a reminder for your appointment with Dr. {appointment.doctor.user.get_full_name()} scheduled for {appointment.date_time.strftime("%Y-%m-%d at %H:%M")}.

        Please arrive 15 minutes before your scheduled appointment.

        Thank you,
        Hospital Team
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email='hospital@example.com',
            recipient_list=[appointment.patient.user.email],
            fail_silently=False,
        )

        return f"Reminder email sent to {appointment.patient.user.email}"
    except Appointment.DoesNotExist:
        return f"Appointment with id {appointment_id} does not exist"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def check_and_send_appointment_reminders():
    """
    Daily task to check for upcoming appointments and send reminders
    """
    from .models import Appointment
    
    # Get appointments for tomorrow
    tomorrow = timezone.now().date() + timedelta(days=1)
    appointments = Appointment.objects.filter(
        date_time__date=tomorrow
    )
    
    for appointment in appointments:
        send_appointment_reminder_email.delay(appointment.id)
    
    return f"Processed {appointments.count()} appointments for reminders"


@shared_task
def update_doctor_availability_cache():
    """
    Task to update the cache of doctor availability
    """
    from .models import Doctor, DoctorSchedule
    
    doctors = Doctor.objects.all()
    availability_data = {}
    
    for doctor in doctors:
        schedules = DoctorSchedule.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date()
        ).values('date', 'start_time', 'end_time')
        
        availability_data[doctor.id] = list(schedules)
    
    # Cache for 1 hour
    cache.set('doctor_availability', availability_data, 3600)
    
    return "Doctor availability cache updated"


@shared_task
def generate_appointment_statistics():
    """
    Task to generate and cache appointment statistics
    """
    from .models import Appointment
    from django.db.models import Count
    
    # Get statistics for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    stats = {
        'total_appointments': Appointment.objects.filter(
            date_time__gte=thirty_days_ago
        ).count(),
        
        'appointments_by_doctor': dict(
            Appointment.objects.filter(date_time__gte=thirty_days_ago)
            .values('doctor__user__first_name', 'doctor__user__last_name')
            .annotate(count=Count('id'))
            .values_list('doctor__user__first_name', 'count')
        ),
        
        'appointments_by_date': dict(
            Appointment.objects.filter(date_time__gte=thirty_days_ago)
            .annotate(date=TruncDate('date_time'))
            .values('date')
            .annotate(count=Count('id'))
            .values_list('date', 'count')
        )
    }
    
    # Cache for 6 hours
    cache.set('appointment_statistics', stats, 21600)
    
    return "Appointment statistics updated"