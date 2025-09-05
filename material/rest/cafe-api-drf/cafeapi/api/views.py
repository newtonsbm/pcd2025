# create drf viewsets for padarias and cestas

from rest_framework import viewsets

from padarias import models
from . import serializers

class PadariaViewSet(viewsets.ModelViewSet):
    queryset = models.Padaria.objects.all()
    serializer_class = serializers.PadariaSerializer

class CestaViewSet(viewsets.ModelViewSet):
    queryset = models.Cesta.objects.all()   
    serializer_class = serializers.CestaSerializer

