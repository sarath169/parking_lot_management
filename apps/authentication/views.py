from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, views
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .forms import SignUpForm

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token
import stripe
from django.views.generic.base import TemplateView
from backend.settings import base

stripe.api_key= base.STRIPE_SECRET_KEY

def account_activation_sent(request):
    return render(request, 'authentication/account_activation_sent.html')


class CreditPageView(TemplateView):
    template_name = "authentication/credit_card.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['key']=base.STRIPE_PUBLISHABLE_KEY

        return context

def charge(request):
    if request.method=='POST':
        charge=stripe.Charge.create(
            amount=2000,
            currency='inr',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
        return render(request, "authentication/charge.html")



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

        return redirect('/auth/login/')
    else:
        return render(request, 'account_activation_invalid.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data.get('email'))

            user.set_password(raw_password=form.cleaned_data.get('password1', None))
            #user.save(commit=False)
            #user = form.save(commit=False)
            user.is_active = False
            user.email=form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('/auth/account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})
# Create your views here.
#def signup(request):
 #   if request.method == 'POST':
  #      form = SignUpForm(request.POST)
   #     if form.is_valid():
    #        user = User.objects.create(username=form.cleaned_data.get('email'))
     #       user.set_password(raw_password=form.cleaned_data.get('password1', None))
      #      user.save()
       #     # user = authenticate(username=user, password=raw_password)
        #    login(request, user)
         #   return redirect('/auth/login/')
    #else:
     #   form = SignUpForm()
    #return render(request, 'authentication/signup.html', {'form': form})
