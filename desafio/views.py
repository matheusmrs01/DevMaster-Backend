import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from desafio.serializers import DesafioSerializer, DesafioMissoesSerializer
from .models import Desafio, DesafioMissoes

from jogador.models import Jogador, JogadorItem

class DesafioViewSet(GenericViewSet):
    queryset = Desafio.objects.all()
    serializer_class = DesafioSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='criarDesafio')
    def CriarDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if (Jogador.objects.get(user=request.user).tipo == 'J'):
            cadastrado = Desafio.objects.filter(nome=desafio['name'])

            if cadastrado.exists():
                return Response({"error": True, "message": "Esse nome de desafio já está em uso."},status=400)
            else:
                jogador_item = JogadorItem.objects.get(pk=int(desafio['item_desafiante']))

                if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                    return Response({"error": True, "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."}, status=400)
                else:
                    desafiado = Jogador.objects.get(pk=int(desafio['desafiado']))
                    if desafiado.tipo == 'J':
                        jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                        jogador_item.save()

                        newDesafio = Desafio()
                        newDesafio.nome = desafio['name']
                        newDesafio.desafiante = Jogador.objects.get(user=request.user)
                        newDesafio.desafiado = desafiado
                        newDesafio.item_desafiante = jogador_item

                        newDesafio.save()
                        serializer = DesafioSerializer(newDesafio)

                        return Response(serializer.data, status=200)
                    else:
                        return Response({"error": True, "message": "O desafiado não é um jogador."}, status=400)

        else:
            return Response({"error": True, "message": "Você não tem permissão para Desafiar alguem."},status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['DELETE'], detail=False, url_path='deletarDesafio')
    def ExcluirDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        try:
            desafioFinded = Desafio.objects.get(pk=desafio['id'])

            if Jogador.objects.get(user=request.user) == desafioFinded.desafiante:
                desafioFinded.delete()

                return Response({"message": "Desafio deletado com sucesso."}, status=200)
            else:
                return Response({"error": True, "message": "Você não é o desafiante do desafio."}, status=400)
        except Desafio.DoesNotExist:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)