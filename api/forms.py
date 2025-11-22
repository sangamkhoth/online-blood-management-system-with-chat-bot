from django import forms
from .models import Hospital, Donor

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'city', 'phone']

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone', 'blood_group', 'city', 'available']
