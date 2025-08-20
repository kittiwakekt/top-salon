from django import forms
from django.utils import timezone
from .models import Appointment, Review, Client, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['master', 'service', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        
        if self.client:
            # Filter services that client has used before or all active services
            self.fields['service'].queryset = Service.objects.filter(is_active=True)
    
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < timezone.now():
            raise forms.ValidationError("Нельзя записаться на прошедшее время")
        return appointment_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['master', 'service', 'rating', 'comment']

class ClientProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Client
        fields = ['phone', 'birth_date', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        client = super().save(commit=False)
        client.user.first_name = self.cleaned_data['first_name']
        client.user.last_name = self.cleaned_data['last_name']
        client.user.email = self.cleaned_data['email']
        
        if commit:
            client.user.save()
            client.save()
        return client