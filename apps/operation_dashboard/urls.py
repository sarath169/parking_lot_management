from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views




app_name = 'operators'
urlpatterns = [
    path('verify/', views.verify, name='verify'),
]
