from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'operators'
urlpatterns = [
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('qr_scanner/', views.QrView.as_view(), name='qr_scanner'),
    #path('parking/', views.parking, name='parking'),
]
