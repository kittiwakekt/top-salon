from rest_framework import generics
from .serializers import (
    SalonSerializer, 
    SalonFullSerializer,
    MasterCreateSerializer,
    MasterListSerializer,
    )
from .models import Salon, Master

class SalonListCreateView(generics.ListCreateAPIView):
    serializer_class = SalonSerializer
    queryset = Salon.objects.filter(is_active=True)

class SalonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SalonFullSerializer
    queryset = Salon.objects.all()

class MasterCreateView(generics.CreateAPIView):
    serializer_class = MasterCreateSerializer
    queryset = Master.objects.all()

class MasterListView(generics.ListAPIView):
    serializer_class = MasterListSerializer
    queryset = Master.objects.all()
