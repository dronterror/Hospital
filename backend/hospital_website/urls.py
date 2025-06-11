from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from hospital import views
from rest_framework import routers
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from hospital.api import views as api_views

# Create the router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'doctors', api_views.DoctorViewSet)
router.register(r'patients', api_views.PatientViewSet)
router.register(r'appointments', api_views.AppointmentViewSet)
router.register(r'services', api_views.ServiceViewSet)

# Create the Wagtail API router
wagtail_api = WagtailAPIRouter('wagtailapi')
wagtail_api.register_endpoint('pages', PagesAPIViewSet)
wagtail_api.register_endpoint('images', ImagesAPIViewSet)
wagtail_api.register_endpoint('documents', DocumentsAPIViewSet)

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="Hospital API",
        default_version='v1',
        description="API documentation for Hospital Management System",
        terms_of_service="https://www.hospital.com/terms/",
        contact=openapi.Contact(email="contact@hospital.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django Admin
    path('django-admin/', admin.site.urls),
    
    # Wagtail Admin and CMS
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('api/v1/', include(router.urls)),
    path('api/v1/wagtail/', wagtail_api.urls),
    
    # REST API endpoints
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    
    # Hospital app URLs
    path('', views.home, name='home'),
    path('hospital/appointment/', views.appointment_form, name='appointment_form'),
    path('hospital/appointment/success/', views.appointment_success, name='appointment_success'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('contact/', views.contact, name='contact'),
    
    # Wagtail CMS pages - should be at the bottom
    path('cms/', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)