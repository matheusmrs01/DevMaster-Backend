from rest_framework import serializers
from desafio.models import Desafio, DesafioMissoes
from jogador.api.serializers import JogadorSerializer
from evento.serializers import ItemSerializer
from missao.api.serializers import MissaoSerializer

class DesafioSerializer(serializers.ModelSerializer):
    desafiante = JogadorSerializer()
    desafiado = JogadorSerializer()
    item_desafiante = ItemSerializer()
    item_desafiado = ItemSerializer()

    class Meta:
        model = Desafio
        fields = '__all__'

    def create(self, validated_data):
        return Desafio.objects.create(**validated_data)

class DesafioMissoesSerializer(serializers.ModelSerializer):
    desafio = DesafioSerializer()
    missao = MissaoSerializer()

    class Meta:
        model = DesafioMissoes
        fields = '__all__'

    def create(self, validated_data):
        return DesafioMissoes.objects.create(**validated_data)