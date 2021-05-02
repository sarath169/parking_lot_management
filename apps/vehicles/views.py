from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64

from .qr_generation import generation
from .forms import AddVehicle
from .models import Vehicle

# Create your views here.

def index(request):
    return render(request,'vehicle/index.html')

def addvehicle(request, user_id):
    if request.method == 'POST':
        form = AddVehicle(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk = user_id)
            veh_number = form.cleaned_data.get('number')
            veh_type = form.cleaned_data.get('type')
            a=Vehicle(number = veh_number, type = veh_type, user = user )
            a.save()
            return redirect('/vehicle/vehicles/')
    else:
        form = AddVehicle()
    return render(request, 'vehicle/add_vehicle.html', {'form': form})

def ListVehicle(request):
    user = request.user
    list = Vehicle.objects.filter(user_id = user.id )
    return render(request,'vehicle/vehicles.html', {"list":list})

# class VehicleView(generic.ListView):
#     # login_url = '/login/'
#     template_name = 'vehicle/vehicles.html'
#     context_object_name = 'vehicles_list'
#
#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Vehicle.objects.all()

# TODO we are saving the image, find another way without saving the image

def return_qr(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    qr = generation(vehicle.number)
    img_name = 'backend/static/vehicles/images/'+str(vehicle.id)+vehicle.number+'.png'
    qr.save(img_name)
    return render(request, 'vehicle/vehicle_qr.html',{'image':img_name})
