from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_appointment_confirmation_email(appointment_id):
    from .models import Appointment

    try:
        appointment = Appointment.objects.get(id=appointment_id)

        subject = f'Appointment Confirmation: {appointment.date} at {appointment.time}'
        message = f'''
        Dear {appointment.patient_name},

        Your appointment with Dr. {appointment.doctor.name} has been confirmed for {appointment.date} at {appointment.time}.

        Please arrive 15 minutes before your scheduled appointment.

        Thank you,
        Hospital Team
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email='hospital@example.com',
            recipient_list=[appointment.contact_email],
            fail_silently=False,
        )

        return f"Confirmation email sent to {appointment.contact_email}"
    except Appointment.DoesNotExist:
        return f"Appointment with id {appointment_id} does not exist"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def send_appointment_reminder_email(appointment_id):
    from .models import Appointment

    try:
        appointment = Appointment.objects.get(id=appointment_id)

        subject = f'Appointment Reminder: {appointment.date} at {appointment.time}'
        message = f'''
        Dear {appointment.patient_name},

        This is a reminder for your appointment with Dr. {appointment.doctor.name} scheduled for {appointment.date} at {appointment.time}.

        Please arrive 15 minutes before your scheduled appointment.

        Thank you,
        Hospital Team
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email='hospital@example.com',
            recipient_list=[appointment.contact_email],
            fail_silently=False,
        )

        return f"Reminder email sent to {appointment.contact_email}"
    except Appointment.DoesNotExist:
        return f"Appointment with id {appointment_id} does not exist"
    except Exception as e:
        return f"Failed to send email: {str(e)}"