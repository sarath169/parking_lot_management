from django.shortcuts import redirect,get_object_or_404
from authentication.models import Payment

def payment_req():
    def decorators(func):
        def wrap(request, *args, **kwargs):
            user=request.user
            
            
            if Payment.objects.filter(user_id = user.id, status='True'):
                return func(request, *args, **kwargs)
            else:                  
                return redirect('/user/')

        return wrap
    return decorators   