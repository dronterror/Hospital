from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, TimeSlotViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'time-slots', TimeSlotViewSet, basename='timeslot')

urlpatterns = [
    path('', include(router.urls)),
] 