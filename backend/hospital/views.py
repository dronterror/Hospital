from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Doctor, Appointment, DoctorSchedule, HomePage, DepartmentPage, ServicePage, NewsPage, Patient, MedicalRecord
from .tasks import send_appointment_confirmation_email, update_doctor_availability_cache, generate_appointment_statistics
import json
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import (
    DoctorSerializer, AppointmentSerializer, DoctorScheduleSerializer,
    DepartmentSerializer, ServiceSerializer, NewsSerializer,
    PatientSerializer, MedicalRecordSerializer
)
from django.db import models
from django.views.generic import DetailView, TemplateView
from django.conf import settings
import os
import csv
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


def home(request):
    """Legacy view that redirects to the Wagtail homepage"""
    from wagtail.models import Site
    site = Site.objects.get(is_default_site=True)
    return redirect(site.root_page.url)


def appointment_form(request):
    """View to handle appointment form"""
    # Get doctors from cache or database
    doctors = cache.get('all_doctors')
    if doctors is None:
        doctors = list(Doctor.objects.all())
        cache.set('all_doctors', doctors, 3600)  # Cache for 1 hour

    if request.method == 'POST':
        patient_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            date_time = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')

            # Create appointment using REST API
            appointment = Appointment.objects.create(
                patient=Patient.objects.get_or_create(
                    user__email=email,
                    defaults={
                        'phone_number': phone,
                    }
                )[0],
                doctor=doctor,
                date_time=date_time,
                reason='Online Booking',
                status='SCHEDULED'
            )

            # Send confirmation email
            send_appointment_confirmation_email.delay(appointment.id)

            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('appointment_success')
        except Exception as e:
            messages.error(request, f'Error scheduling appointment: {str(e)}')

    return render(request, 'hospital/appointment.html', {'doctors': doctors})


def appointment_success(request):
    """View to show successful appointment booking"""
    return render(request, 'hospital/appointment_success.html')


@cache_page(60 * 15)  # Cache for 15 minutes
def doctor_list(request):
    """View to list all doctors"""
    doctors = Doctor.objects.all()
    return render(request, 'hospital/doctors.html', {'doctors': doctors})


def calendar_view(request):
    """View to render calendar page"""
    return render(request, 'hospital/calendar.html')


@cache_page(60 * 5)  # Cache for 5 minutes
def calendar_data(request):
    """API view to provide calendar data"""
    # Try to get data from cache
    events = cache.get('calendar_events')
    
    if events is None:
        schedules = DoctorSchedule.objects.select_related('doctor').all()
        events = []

        for schedule in schedules:
            events.append({
                'title': f'Dr. {schedule.doctor.name}',
                'start': f'{schedule.date.isoformat()}T{schedule.start_time.isoformat()}',
                'end': f'{schedule.date.isoformat()}T{schedule.end_time.isoformat()}',
            })
        
        # Cache for 5 minutes
        cache.set('calendar_events', events, 300)

    return JsonResponse(events, safe=False)


def contact(request):
    """View to render contact page"""
    return render(request, 'hospital/contact.html')


def statistics(request):
    """View to show appointment statistics"""
    stats = cache.get('appointment_statistics')
    
    if stats is None:
        # If stats are not in cache, generate them asynchronously
        generate_appointment_statistics.delay()
        # Return empty stats for now
        stats = {
            'total_appointments': 0,
            'appointments_by_doctor': {},
            'appointments_by_date': {}
        }
    
    return render(request, 'hospital/statistics.html', {'stats': stats})


# API ViewSets
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__email', 'date_of_birth']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['created_at', 'user__last_name']


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'license_number']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    ordering_fields = ['created_at', 'user__last_name']


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'date_time', 'doctor', 'patient']
    search_fields = ['reason', 'notes']
    ordering_fields = ['date_time', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(
            Q(patient__user=self.request.user) | 
            Q(doctor__user=self.request.user)
        )

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        appointments = self.get_queryset()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="appointments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Time', 'Patient', 'Doctor', 'Status', 'Notes'])
        
        for appointment in appointments:
            writer.writerow([
                appointment.date_time.strftime('%Y-%m-%d'),
                appointment.date_time.strftime('%H:%M'),
                f"{appointment.patient.user.get_full_name()}",
                f"Dr. {appointment.doctor.user.get_full_name()}",
                appointment.status,
                appointment.notes
            ])
        
        return response


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'doctor', 'patient']
    search_fields = ['diagnosis', 'prescription', 'notes']
    ordering_fields = ['date', 'created_at']


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor', None)
        date = self.request.query_params.get('date', None)

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset


# Custom API Views
class AvailableSlotsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        doctor_id = request.query_params.get('doctor')
        date = request.query_params.get('date')

        if not doctor_id or not date:
            return Response(
                {"error": "Both doctor and date parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache_key = f'available_slots_{doctor_id}_{date}'
        available_slots = cache.get(cache_key)

        if available_slots is None:
            doctor = get_object_or_404(Doctor, id=doctor_id)
            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                date=date,
                is_available=True
            )
            available_slots = [
                {
                    'start_time': schedule.start_time,
                    'end_time': schedule.end_time
                }
                for schedule in schedules
            ]
            cache.set(cache_key, available_slots, timeout=300)  # Cache for 5 minutes

        return Response(available_slots)


class BookAppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the slot is still available
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']

            if Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time
            ).exists():
                return Response(
                    {"error": "This slot is no longer available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            appointment = serializer.save()
            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListView(generics.ListAPIView):
    queryset = DepartmentPage.objects.live()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]


class ServiceListView(generics.ListAPIView):
    queryset = ServicePage.objects.live()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


class NewsListView(generics.ListAPIView):
    queryset = NewsPage.objects.live().order_by('-date')
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]


class SPAView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current URL path to the frontend app
        context['REACT_APP_API_URL'] = 'http://api.hospital.localhost/api'
        context['INITIAL_PATH'] = self.request.path
        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except:
            # If the template is not found in the Django templates directory,
            # try to serve it from the React build directory
            index_file = os.path.join(settings.BASE_DIR.parent, 'frontend', 'build', 'index.html')
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    return HttpResponse(f.read())


class DoctorAvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        doctor_id = request.query_params.get('doctor')
        date_str = request.query_params.get('date')

        if not doctor_id or not date_str:
            return Response(
                {"error": "Both doctor and date parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            doctor = Doctor.objects.get(id=doctor_id)
            
            # Get all appointments for the doctor on the specified date
            booked_slots = Appointment.objects.filter(
                doctor=doctor,
                date_time__date=date,
                status='SCHEDULED'
            ).values_list('date_time__time', flat=True)
            
            # Generate available time slots (9 AM to 5 PM, 30-minute intervals)
            available_slots = []
            current_time = datetime.strptime('09:00', '%H:%M').time()
            end_time = datetime.strptime('17:00', '%H:%M').time()
            
            while current_time < end_time:
                if current_time not in booked_slots:
                    available_slots.append(current_time.strftime('%H:%M'))
                current_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()
            
            return Response({
                'doctor_id': doctor_id,
                'date': date_str,
                'available_slots': available_slots
            })
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )