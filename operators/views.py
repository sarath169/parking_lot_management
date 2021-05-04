from django.shortcuts import render, redirect
from django.contrib.auth.models import User , Group
from pyzbar import pyzbar
import cv2
from django.views import View
# Create your views here.

class VerifyView(View):
    def get(self,request):
        try:
            enter=request.user
            user=User.objects.get(id=enter.id)
            group=Group.objects.get(id=1)

            #user_id=group_id.user_id
            #print(user_id)
            group_1=user.groups.get(id=group.id)

            return render(request, 'operator/op_dashboard.html')

        except:
            return redirect('/user/')


class QrView(View):

    template_name= 'operator/op_dashboard.html'

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
                x, y , w, h = qrcode.rect
                #4-create boundary around qrcode
                qrcode_info = qrcode.data.decode('utf-8')
                cv2.rectangle(frame, (x, y),(x + w, y + h), (0, 255, 0), 2)
                #5-decode qr and show the result
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, qrcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            if qrcode_info:
                print(qrcode_info)
            cv2.imshow('QR code reader', frame)

            #6-help to close the camera
            if cv2.waitKey(1) & 0xFF == 27:
                break

            if qrcode_info is not None:
                break


        camera.release()
        cv2.destroyAllWindows()
        return render(request, self.template_name)
