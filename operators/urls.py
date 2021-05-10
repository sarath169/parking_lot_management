from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'operators'
urlpatterns = [
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('scanner/', views.entryscanner, name = 'scanner'),
    path('exit/', views.exitscanner, name='exit'),
    path('entry/', views.EntryCreateAPIView.as_view()),
    path('exitupdate/', views.ExitUpdateAPIView.as_view()),
    #path('parking/', views.parking, name='parking'),
]
