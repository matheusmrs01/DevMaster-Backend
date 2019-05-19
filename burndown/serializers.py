from rest_framework import serializers
from .models import Burndown, MissaoBurndown
from missao.api.serializers import MissaoSerializer

class BurndownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Burndown
        fields = '__all__'

class MissaoBurndownSerializer(serializers.ModelSerializer):
    burndown = BurndownSerializer()
    missao = MissaoSerializer()

    class Meta:
        model = MissaoBurndown
        fields = '__all__'