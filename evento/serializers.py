from rest_framework import serializers
from evento.models import *

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    name = serializers.CharField(required=True, max_length=200)
    descricao = serializers.CharField(required=False)
    url_image = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = ('id', 'name', 'descricao', 'url_image',)

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ["__all__"]

        def create(self, validated_data):
            return Evento.objects.create(**validated_data)