# create drf serializers

from rest_framework import serializers
from padarias import models


class PadariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Padaria
        fields = '__all__'

class CestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cesta
        fields = '__all__'
