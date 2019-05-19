from rest_framework import serializers
from missao.models import Missao
from jogador.models import Jogador


class MissaoSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Missao.objects.all())
    jogador = serializers.PrimaryKeyRelatedField(queryset=Jogador.objects.all(), many=False)

    class Meta:
        model = Missao
        fields = ('id', 'jogador', 'nome_missao', 'xp_missao', 'data', 'nice_tempo', 'status', 'id_issue', 'id_projeto')

class CriarMissaoSerializer(serializers.ModelSerializer):
    jogador = serializers.PrimaryKeyRelatedField(queryset=Jogador.objects.all(), many=False)

    class Meta:
        model = Missao
        fields = ('jogador', 'nome_missao', 'xp_missao', 'data', 'status', 'nice_tempo', 'id_issue', 'id_projeto')

