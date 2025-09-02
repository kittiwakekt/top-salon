from django import forms
from .models import Salon, Master, Service, MasterService

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = '__all__'
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MasterServiceForm(forms.ModelForm):
    class Meta:
        model = MasterService
        fields = '__all__'