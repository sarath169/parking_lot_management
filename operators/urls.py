from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'operators'
urlpatterns = [
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('entry/', views.EntryView.as_view(), name='entry'),
    path('exit/', views.ExitView.as_view(), name='exit'),
    #path('parking/', views.parking, name='parking'),
]
