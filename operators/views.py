import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User , Group
from django.utils import timezone
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from parking import views
from parking.views import charge
from user_dash.models import Vehicle
from parking.models import ParkingHistory
from django.core.exceptions import ObjectDoesNotExist

from .forms import QRForm


# Create your views here.

class VerifyView(View):

    def get(self,request):
        try:
            enter=request.user
            user=User.objects.get(id=enter.id)
            group=Group.objects.get(id=1)
            group_1=user.groups.get(id=group.id)
            return render(request, 'operator/op_dashboard.html')
        except:
            return redirect('/user/')

def entryscanner(request):
    print("in the entryscanner")
    if request.method == 'POST':
        print("in the entryscanner")
        form = QRForm(request.POST)
        if form.is_valid():
            veh_number = form.cleaned_data.get('qrdata')
            vehicle = get_object_or_404(Vehicle, number = veh_number)
            print("in the entryscanner")
            print(veh_number)
            if ParkingHistory.objects.filter(vehicle_id = vehicle.id, out_datetime = None):
                return render(request, 'operator/qr_scanner.html',{'error_message':'Vehicle already entered in parking'})
            else:
                entry_object = ParkingHistory(vehicle = vehicle)
                entry_object.save()
                return render(request, 'operator/qr_scanner.html')
    else:
        form = QRForm()
    return render(request, 'operator/qr_scanner.html', {'form': form})

def exitscanner(request):
    if request.method == 'POST':
        form = QRForm(request.POST)
        if form.is_valid():
            veh_number = form.cleaned_data.get('qrdata')
            vehicle = get_object_or_404(Vehicle, number = veh_number)
            print("in the exitscanner")
            try:
                exit_updation = ParkingHistory.objects.get(vehicle_id = vehicle.id, out_datetime = None)
                exit_updation.out_datetime = timezone.now()
                exit_updation.charges =charge(exit_updation.in_datetime, exit_updation.out_datetime)
                exit_updation.save()

            except ObjectDoesNotExist:
                print("ObjectDoesNotExist")
                return render(request, 'operator/qr_scanner.html',{'error_message':"There is no entry record"})

            return render(request, 'operator/qr_scanner.html')
    else:
        form = QRForm()
    return render(request, 'operator/qr_scanner.html', {'form': form})
