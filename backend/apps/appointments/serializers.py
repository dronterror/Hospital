from rest_framework import serializers
from .models import Appointment, TimeSlot
from apps.doctors.serializers import DoctorSerializer
from apps.patients.serializers import PatientSerializer

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start_time', 'end_time', 'is_available']
        read_only_fields = ['is_available']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)
    time_slot_details = TimeSlotSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'appointment_date', 'time_slot',
            'status', 'priority', 'reason', 'symptoms', 'notes',
            'prescription', 'follow_up_date', 'cancelled_by',
            'cancellation_reason', 'created_at', 'updated_at',
            'doctor_details', 'patient_details', 'time_slot_details'
        ]
        read_only_fields = ['cancelled_by', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validate appointment data.
        """
        # Check if the time slot belongs to the selected doctor
        if data.get('time_slot') and data.get('doctor'):
            if data['time_slot'].doctor != data['doctor']:
                raise serializers.ValidationError({
                    'time_slot': 'This time slot does not belong to the selected doctor.'
                })

        # Check if the time slot is available
        if data.get('time_slot') and not data['time_slot'].is_available:
            raise serializers.ValidationError({
                'time_slot': 'This time slot is not available.'
            })

        return data

class AppointmentActionSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False, allow_blank=True)
    prescription = serializers.CharField(required=False, allow_blank=True)
    follow_up_date = serializers.DateField(required=False, allow_null=True)
    cancellation_reason = serializers.CharField(required=False, allow_blank=True)
    new_date = serializers.DateField(required=False)
    new_time_slot = serializers.PrimaryKeyRelatedField(
        queryset=TimeSlot.objects.all(),
        required=False
    )

    def validate(self, data):
        action = self.context.get('action')
        if action == 'cancel' and not data.get('cancellation_reason'):
            raise serializers.ValidationError({
                'cancellation_reason': 'Cancellation reason is required.'
            })
        elif action == 'reschedule':
            if not data.get('new_date'):
                raise serializers.ValidationError({
                    'new_date': 'New date is required for rescheduling.'
                })
            if not data.get('new_time_slot'):
                raise serializers.ValidationError({
                    'new_time_slot': 'New time slot is required for rescheduling.'
                })
        return data 