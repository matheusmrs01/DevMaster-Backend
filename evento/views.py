import base64
import imghdr
import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from evento.serializers import EventoSerializer, ItemSerializer
from evento.models import Evento, Item

class ItemViewSet(GenericViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='criarItem')
    def CriarItem(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            item = jsonData
        else:
            item = request.POST.get('item')

        cadastrado = Item.objects.filter(name=item['name'])

        if cadastrado.exists():
            return Response(
                {"error": True, "message": "Esse Objeto existe."},
                status=400)
        else:
            newItem = Item()
            newItem.name = item['name']
            newItem.descricao = item['descricao']
            newItem.url_image = item['url_image']

            newItem.save()

            serializer = ItemSerializer(newItem)
            return Response(serializer.data, status=200)