from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),

    # Wagtail admin
    path('admin/', include(wagtailadmin_urls)),

    # Wagtail documents
    path('documents/', include(wagtaildocs_urls)),

    # Hospital app URLs
    path('hospital/', include('hospital.urls')),

    # For anything not caught by the above, fall back to Wagtail's page serving
    path('', include(wagtail_urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)