from django import forms

from .models import Device

class AddDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('dev_eui', 'address')

class SearchDeviceForm(forms.ModelForm):
    
    dev_eui = forms.CharField(required=False)
    
    class Meta:
        model = Device
        fields = ('dev_eui', 'address')
        
class EditDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('address',)
        
class DeleteDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('dev_eui',)