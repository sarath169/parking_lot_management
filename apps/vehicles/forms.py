from django import forms

vehicle_type= [
    (2, '2 Wheeler'),
    (4, '4 Wheeler'),
    ]
class AddVehicle(forms.Form):

    number = forms.CharField(label='Vehicle_Reg_Number',max_length=128)
    type= forms.IntegerField(label='Vehicle_Type', widget=forms.Select(choices=vehicle_type))
    
