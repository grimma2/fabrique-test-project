from rest_framework import generics

from .models import Client
from .serializers import ClientSerializer


class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientUpdateView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDeleteView(generics.DestroyAPIView):
    queryset = Client.objects.all()