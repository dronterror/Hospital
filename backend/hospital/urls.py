from django.urls import path
from . import views

urlpatterns = [
    # Legacy URLs
    path('old/', views.home, name='old-home'),
    path('appointment/', views.appointment_form, name='appointment'),
    path('appointment/success/', views.appointment_success, name='appointment-success'),
    path('doctors/', views.doctor_list, name='doctors'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/data/', views.calendar_data, name='calendar-data'),
    path('contact/', views.contact, name='contact'),
]