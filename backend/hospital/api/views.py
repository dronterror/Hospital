from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Doctor, Patient, Appointment, Service
from ..serializers import (
    DoctorSerializer,
    PatientSerializer,
    AppointmentSerializer,
    ServiceSerializer
)

class DoctorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to be viewed or edited.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        doctor = self.get_object()
        appointments = doctor.appointments.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        doctor = self.get_object()
        return Response({
            'available_slots': doctor.get_available_slots(),
            'working_hours': doctor.working_hours
        })

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all patients
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=user)

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        patient = self.get_object()
        appointments = patient.appointments.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows appointments to be viewed or edited.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all appointments
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient__user=user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'status': 'appointment cancelled'})

class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        service = self.get_object()
        doctors = service.doctors.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data) 