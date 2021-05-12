import stripe
import threading

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, views
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from .tokens import account_activation_token
from .forms import SignUpForm
from .models import Payment


stripe.api_key= settings.STRIPE_SECRET_KEY


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def home(request):

    return render(request, 'authentication/home.html')

class CreditPageView(TemplateView):
    template_name = "authentication/credit_card.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['key']=settings.STRIPE_PUBLISHABLE_KEY

        return context

def charge(request):
    if request.method=='POST':
        charge=stripe.Charge.create(
            amount=2000,
            currency='inr',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
        user=request.user
        payment=Payment( user= user, status=True)
        payment.save()

        return redirect('/user/')


def account_activation_sent(request):

    return render(request, 'authentication/account_activation_sent.html')

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

        return redirect('/auth/credit_card/')

    else:

        return render(request, 'account_activation_invalid.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data.get('email'))
            raw_password=user.set_password(raw_password=form.cleaned_data.get('password1', None))
            user.is_active = False
            user.email=form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            subject = 'Parking App  : Account Activated Successfully.'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            to=user.email
            email= EmailMessage(
                subject,
                message,
                email_from,
                [to]
            )
            EmailThread(email).start()

            return redirect('/auth/account_activation_sent')

    else:
        form = SignUpForm()
        
    return render(request, 'authentication/signup.html', {'form': form})
