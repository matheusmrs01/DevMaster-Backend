from rest_framework import serializers
from .models import Burndown
from missao.api.serializers import MissaoSerializer

class BurndownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Burndown
        fields = '__all__'
