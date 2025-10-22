from rest_framework import serializers
from .models import Salon, Master, Service, MasterService

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        exclude = ['is_active']

class SalonFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'

class MasterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ['id', 
                  'first_name', 
                  'last_name', 
                  'specialization',
                  'experience',
                  'salon',
                  'hire_date',
                  ]
    

class MasterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
    
     
     
     

