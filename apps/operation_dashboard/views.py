from django.shortcuts import render, redirect
from django.contrib.auth.models import User , Group

# Create your views here.


def verify(request):
    try:
        enter=request.user
        user=User.objects.get(id=enter.id)
        group=Group.objects.get(id=1)
    
        #user_id=group_id.user_id
        #print(user_id)
        group_1=user.groups.get(id=group.id)
        return render(request, 'authentication/op_dashboard.html')
    
    except:
        return redirect('/operators/non_operator/')    

def non_operator(request):
    return render(request, 'authentication/non_operator.html')      
 