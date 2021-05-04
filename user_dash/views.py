from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64

from .qr_generator import generation
from .forms import AddVehicle
from .models import Vehicle

# Create your views here.
@login_required
def index(request):
    login_url = '/login/'
    return render(request,'user_dash/index.html')

@login_required
def addvehicle(request, user_id):
    login_url = '/login/'
    if request.method == 'POST':
        form = AddVehicle(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk = user_id)
            veh_number = form.cleaned_data.get('number')
            veh_type = form.cleaned_data.get('type')
            a=Vehicle(number = veh_number, type = veh_type, user = user )
            a.save()
            return redirect('/user/vehicles/')
    else:
        form = AddVehicle()
    return render(request, 'user_dash/add_vehicle.html', {'form': form})

@login_required
def ListVehicle(request):
    login_url = '/login/'
    user = request.user
    list = Vehicle.objects.filter(user_id = user.id )
    return render(request,'user_dash/vehicles.html', {"list":list})

def return_qr(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    qr = generation(vehicle.number)
    # img_name = 'media/images/'+str(vehicle.id)+vehicle.number+'.png'
    img_name = 'http://127.0.0.1:8000/media/images/1ap16bp9591.png'
    # qr.save(img_name)
    return render(request, 'user_dash/vehicle_qr.html',{'image':img_name})
