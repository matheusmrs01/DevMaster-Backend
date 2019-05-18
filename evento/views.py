import base64
import imghdr
import json
from datetime import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

from evento.serializers import EventoSerializer, ItemSerializer
from evento.models import Evento, Item

from django.contrib.auth.models import User
from jogador.models import Jogador

class ItemViewSet(GenericViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='criarItem')
    def CriarItem(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            item = jsonData
        else:
            item = request.POST.get('item')

        if(Jogador.objects.get(user=request.user).tipo == 'A'):
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
        else:
            return Response(
                {"error": True, "message": "Você não tem permissão para criar um item."},
                status=400)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarItens')
    def consultarItens(self, request):
        itens = Item.objects.all()
        serializer = ItemSerializer(itens, many=True)
        return Response({"list": serializer.data})

    @method_decorator(csrf_exempt)
    @action(methods=['PUT'], detail=False, url_path='atualizarItem')
    def atualizarItem(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            item = jsonData
        else:
            item = request.POST.get('item')

        if (Jogador.objects.get(user=request.user).tipo == 'A'):
            itemFinded = Item.objects.get(pk=item['id'])

            if not(itemFinded.name != item['name'] and Item.objects.filter(name=item['name'])):
                itemFinded.name = item['name']
                itemFinded.descricao = item['descricao']
                itemFinded.urlImage = item['url_image']
                itemFinded.save()

                serializer = ItemSerializer(itemFinded)
                return Response({'Item:': serializer.data}, status=200)
            else:
                return Response(
                    {"message": "Esse nome ja esta em uso."},
                    status=400)

        else:
            return Response(
                {"message": "Você não tem permissão para criar um item."},
                status=400)

    @method_decorator(csrf_exempt)
    @action(methods=['DELETE'], detail=False, url_path='deletarItem')
    def deletarItem(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            item = jsonData
        else:
            item = request.POST.get('item')

        if (Jogador.objects.get(user=request.user).tipo == 'A'):
            itemFinded = Item.objects.get(pk=item['id'])
            itemFinded.delete()
            return Response({"message": "Item deletado com sucesso."})

        else:
            return Response(
                {"message": "Você não tem permissão para criar um item."},
                status=400)

class EventoViewSet(GenericViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #dando erro
    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='criarEvento')
    def criarEvento(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            evento = jsonData
        else:
            evento = request.POST.get('item')

        if (Jogador.objects.get(user=request.user).tipo == 'A'):
            cadastrado = Evento.objects.filter(name=evento['name'])

            if cadastrado.exists():
                return Response(
                    {"error": True, "message": "Esse Evento já existe."},
                    status=400)
            else:
                newEvento = Evento()
                newEvento.name = evento['name']
                newEvento.is_active = evento['is_active']
                newEvento.multiplicador_xp = evento['multiplicador_xp']
                newEvento.data_inicio = datetime.now()
                newEvento.primeiro = Item.Object.get(pk=evento['primeiro'])
                newEvento.segundo = Item.Object.get(pk=evento['segundo'])
                newEvento.terceiro = Item.Object.get(pk=evento['terceiro'])
                newEvento.quarto = Item.Object.get(pk=evento['quarto'])
                newEvento.quinto = Item.Object.get(pk=evento['quinto'])
                newEvento.sexto = Item.Object.get(pk=evento['sexto'])

                newEvento.save()

                serializer = EventoSerializer(newEvento)
                return Response(serializer.data, status=200)
        else:
            return Response(
                {"error": True, "message": "Você não tem permissão para criar um evento."},
                status=400)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarEventos')
    def consultarEventos(self, request):
        eventos = Evento.objects.all()
        serializer = EventoSerializer(eventos, many=True)
        return Response({"list": serializer.data})

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarEvento')
    def consultarEvento(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            evento = jsonData
        else:
            evento = request.POST.get('item')

        eventoFidend = Evento.objects.get(pk=evento['id'])
        print(evento['id'])
        serializer = EventoSerializer(eventoFidend)
        return Response({'Evento: ': serializer.data})