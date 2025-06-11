from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Appointment, TimeSlot
from .serializers import (
    AppointmentSerializer,
    TimeSlotSerializer,
    AppointmentActionSerializer
)
from .permissions import IsAppointmentParticipant

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['doctor', 'is_available']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']
    ordering_fields = ['start_time', 'end_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date')
        doctor_id = self.request.query_params.get('doctor')

        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                # Get appointments for the specified date
                appointments = Appointment.objects.filter(
                    appointment_date=date_obj,
                    status__in=['scheduled', 'confirmed']
                )
                # Exclude time slots that are already booked
                queryset = queryset.exclude(appointments__in=appointments)
            except ValueError:
                pass

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAppointmentParticipant]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'doctor', 'patient', 'appointment_date']
    search_fields = [
        'doctor__user__first_name', 'doctor__user__last_name',
        'patient__user__first_name', 'patient__user__last_name',
        'reason', 'symptoms'
    ]
    ordering_fields = ['appointment_date', 'created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.user_type == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.user_type in ['admin', 'staff']:
            return Appointment.objects.all()
        return Appointment.objects.none()

    def perform_create(self, serializer):
        # Check if the time slot is still available
        time_slot = serializer.validated_data['time_slot']
        if not time_slot.is_available:
            raise serializers.ValidationError({
                'time_slot': 'This time slot is no longer available.'
            })
        
        # Create the appointment
        appointment = serializer.save()
        
        # Mark the time slot as unavailable
        time_slot.is_available = False
        time_slot.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        serializer = AppointmentActionSerializer(
            data=request.data,
            context={'action': 'cancel'}
        )
        
        if serializer.is_valid():
            appointment.cancel(
                cancelled_by=request.user,
                reason=serializer.validated_data['cancellation_reason']
            )
            return Response({'status': 'Appointment cancelled'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        serializer = AppointmentActionSerializer(data=request.data)
        
        if serializer.is_valid():
            appointment.complete(
                notes=serializer.validated_data.get('notes'),
                prescription=serializer.validated_data.get('prescription'),
                follow_up_date=serializer.validated_data.get('follow_up_date')
            )
            return Response({'status': 'Appointment completed'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        serializer = AppointmentActionSerializer(
            data=request.data,
            context={'action': 'reschedule'}
        )
        
        if serializer.is_valid():
            appointment.reschedule(
                new_date=serializer.validated_data['new_date'],
                new_time_slot=serializer.validated_data['new_time_slot']
            )
            return Response({'status': 'Appointment rescheduled'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments for the current user."""
        user = request.user
        today = timezone.now().date()
        
        if user.user_type == 'doctor':
            appointments = Appointment.objects.filter(
                doctor__user=user,
                appointment_date__gte=today,
                status__in=['scheduled', 'confirmed']
            )
        elif user.user_type == 'patient':
            appointments = Appointment.objects.filter(
                patient__user=user,
                appointment_date__gte=today,
                status__in=['scheduled', 'confirmed']
            )
        else:
            appointments = Appointment.objects.filter(
                appointment_date__gte=today,
                status__in=['scheduled', 'confirmed']
            )

        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """Get available time slots for a specific doctor and date."""
        doctor_id = request.query_params.get('doctor')
        date_str = request.query_params.get('date')

        if not doctor_id or not date_str:
            return Response(
                {'error': 'Both doctor and date parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all time slots for the doctor
        time_slots = TimeSlot.objects.filter(
            doctor_id=doctor_id,
            is_available=True
        )

        # Exclude time slots that are already booked
        booked_slots = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=date,
            status__in=['scheduled', 'confirmed']
        ).values_list('time_slot_id', flat=True)

        available_slots = time_slots.exclude(id__in=booked_slots)
        serializer = TimeSlotSerializer(available_slots, many=True)
        
        return Response(serializer.data) 