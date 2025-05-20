from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Doctor, Appointment, DoctorSchedule
import json
from datetime import datetime


def home(request):
    """Legacy view that redirects to the Wagtail homepage"""
    from wagtail.models import Site
    site = Site.objects.get(is_default_site=True)
    return redirect(site.root_page.url)


def appointment_form(request):
    """View to handle appointment form"""
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        patient_name = request.POST.get('name')
        email = request.POST.get('email')
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()

            # Create appointment
            appointment = Appointment.objects.create(
                patient_name=patient_name,
                contact_email=email,
                doctor=doctor,
                date=date,
                time=time
            )

            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('appointment-success')
        except Exception as e:
            messages.error(request, f'Error scheduling appointment: {str(e)}')

    return render(request, 'hospital/appointment.html', {'doctors': doctors})


def appointment_success(request):
    """View to show successful appointment booking"""
    return render(request, 'hospital/appointment_success.html')


def doctor_list(request):
    """View to list all doctors"""
    doctors = Doctor.objects.all()
    return render(request, 'hospital/doctors.html', {'doctors': doctors})


def calendar_view(request):
    """View to render calendar page"""
    return render(request, 'hospital/calendar.html')


def calendar_data(request):
    """API view to provide calendar data"""
    schedules = DoctorSchedule.objects.select_related('doctor').all()
    events = []

    for schedule in schedules:
        events.append({
            'title': f'Dr. {schedule.doctor.name}',
            'start': f'{schedule.date.isoformat()}T{schedule.start_time.isoformat()}',
            'end': f'{schedule.date.isoformat()}T{schedule.end_time.isoformat()}',
        })

    return JsonResponse(events, safe=False)


def contact(request):
    """View to render contact page"""
    return render(request, 'hospital/contact.html')