from rest_framework import serializers
from wagtail.images.shortcuts import get_rendition_or_not_found
from django.contrib.auth.models import User
from .models import (
    Doctor, Appointment, DoctorSchedule, DepartmentPage,
    ServicePage, NewsPage, Patient, MedicalRecord
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.title', read_only=True)
    photo_url = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'department', 'department_name',
            'photo_url', 'bio', 'email', 'phone', 'is_active', 'user'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            return get_rendition_or_not_found(obj.photo, 'fill-200x200').url
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor


class DoctorScheduleSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = [
            'id', 'doctor', 'doctor_name', 'date', 'start_time',
            'end_time', 'is_available'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        write_only=True,
        source='patient'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='doctor'
    )
    dateTime = serializers.DateTimeField(source='date_time')

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'dateTime', 'status',
            'notes', 'patient_id', 'doctor_id'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Check that the appointment time is available.
        """
        if Appointment.objects.filter(
            doctor=data['doctor'],
            date_time=data['date_time']
        ).exists():
            raise serializers.ValidationError(
                "This time slot is already booked."
            )
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentPage
        fields = ['id', 'title', 'description', 'image_url', 'url']

    def get_image_url(self, obj):
        if obj.image:
            return get_rendition_or_not_found(obj.image, 'fill-800x450').url
        return None


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePage
        fields = ['id', 'title', 'description', 'icon', 'price', 'duration', 'url']


class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = NewsPage
        fields = ['id', 'title', 'date', 'intro', 'body', 'image_url', 'url']

    def get_image_url(self, obj):
        if obj.image:
            return get_rendition_or_not_found(obj.image, 'fill-800x450').url
        return None


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        write_only=True,
        source='patient'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='doctor'
    )

    class Meta:
        model = MedicalRecord
        fields = '__all__' 