from rest_framework import serializers
from missao.models import Missao, Grupo
from jogador.models import Jogador
from jogador.api.serializers import JogadorSerializer


class MissaoSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Missao.objects.all())
    jogador = JogadorSerializer()

    class Meta:
        model = Missao
        fields = ('id', 'jogador', 'nome_missao', 'xp_missao', 'data', 'nice_tempo', 'nice_data', 'xp_ganha', 'status', 'id_issue', 'id_projeto', 'id_milestone')

class CriarMissaoSerializer(serializers.ModelSerializer):
    jogador = serializers.PrimaryKeyRelatedField(queryset=Jogador.objects.all(), many=False)

    class Meta:
        model = Missao
        fields = ('jogador', 'nome_missao', 'xp_missao', 'data', 'status', 'nice_tempo', 'id_issue', 'id_projeto', 'id_milestone')

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'