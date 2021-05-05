import cv2

from django.shortcuts import render, redirect
from django.contrib.auth.models import User , Group
from django.views import View
from pyzbar import pyzbar

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

class QrView(View):

    template_name= 'operator/parking.html'
    template_name1='operator/op_dashboard.html'
    def get(self,request):
        #1-turning on the camera of the computer using OpenCV
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        #2-loop to keep running the decoding function until the “Esc” key is pressed or the code is decode.
        while ret:
            ret, frame = camera.read()
            qrcode_info=None
            #3-start decode the qrcode
            qrcodes = pyzbar.decode(frame)
            for qrcode in qrcodes:
                qrcode_info = qrcode.data.decode('utf-8')              
            cv2.imshow('QR code reader', frame)
            #4-help to close the camera
            if cv2.waitKey(1) & 0xFF == 27:                
                break
                 
            if qrcode_info:
                camera.release()
                cv2.destroyAllWindows()   
                return render(request, self.template_name, {'qrcode_info':qrcode_info}) 
        camera.release() 
        cv2.destroyAllWindows()                     
        return render(request, self.template_name1)
        
            
        
