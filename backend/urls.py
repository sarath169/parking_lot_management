from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('operators/', include('apps.operation_dashboard.urls')),
    path('vehicle/', include('apps.vehicles.urls')),
]
