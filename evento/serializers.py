from rest_framework import serializers
from evento.models import *

class ItemSerializer(serializers.Serializer):
    class Meta:
        model = Item
        fields = ["__all__"]

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

class EventoSerializer(serializers.Serializer):
    class Meta:
        model = Evento
        fields = ["__all__"]

        def create(self, validated_data):
            return Evento.objects.create(**validated_data)