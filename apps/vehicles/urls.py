from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'vehicle'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:user_id>/add/', views.addvehicle, name='add_vehicle'),
    path('vehicles/', views.VehicleView.as_view(), name = 'view_vehicles' ),
    path('<int:vehicle_id>/qrcode/', views.return_qr, name = 'return_qr'),

]
