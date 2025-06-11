from rest_framework import permissions

class IsAppointmentParticipant(permissions.BasePermission):
    """
    Custom permission to only allow doctors and patients to access their own appointments.
    Admin and staff users can access all appointments.
    """

    def has_permission(self, request, view):
        # Allow authenticated users only
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin and staff can do anything
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their own appointments
        if request.user.user_type == 'doctor':
            return obj.doctor.user == request.user

        # Patients can only access their own appointments
        if request.user.user_type == 'patient':
            return obj.patient.user == request.user

        return False 