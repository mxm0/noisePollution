from django import forms

from .models import Device

class AddDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('dev_eui', 'address')

class SearchDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('dev_eui', 'address')
        
class EditDeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ('address',)