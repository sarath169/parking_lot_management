from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
