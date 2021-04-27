from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views as core_views
from . import views


app_name = 'auth'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('credit_card/',views.credit_card, name = 'credit_card'),
    path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),

]
