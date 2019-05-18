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


    @method_decorator(csrf_exempt)
    @action(methods=['PUT'], detail=False, url_path='editarDesafio')
    def EditarDesafio(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        if Desafio.objects.get(pk=desafio['id']):
            desafioFinded = Desafio.objects.get(pk=desafio['id'])
            jogadorFinded = Jogador.objects.get(user=request.user)
            if jogadorFinded.tipo == 'J':
                if jogadorFinded == desafioFinded.desafiado:
                    #quando o jogador vai adicionar o item no desafio pela primeira vez
                    if not desafioFinded.item_desafiado:
                        if JogadorItem.objects.get(pk=int(desafio['item'])):
                            jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))
                            if jogador_item.jogador == jogadorFinded:
                                if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                    return Response({"error": True, "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."}, status=400)
                                else:
                                    jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                    jogador_item.save()

                                    desafioFinded.item_desafiado = jogador_item
                                    desafioFinded.save()

                                    serializer = DesafioSerializer(desafioFinded)

                                    return Response(serializer.data, status=200)
                            else:
                                return Response({"error": True,
                                                 "message": "Esse item não pertence a esse jogador."},
                                                status=400)
                        else:
                            return Response({"error": True,
                                             "message": "Esse item não existe para esse jogador."},
                                            status=400)
                    #quando o jogador vai alterar o item do desafio
                    else:
                        if JogadorItem.objects.get(pk=int(desafio['item'])):
                            jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))

                            if jogador_item.jogador == jogadorFinded:
                                if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                    return Response({"error": True,
                                                     "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."},
                                                    status=400)
                                else:
                                    jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                    jogador_item.save()

                                    jogador_item_old = JogadorItem.objects.get(pk=desafioFinded.item_desafiado.id)
                                    jogador_item_old.quantidade_bloqueada = jogador_item_old.quantidade_bloqueada - 1
                                    jogador_item_old.save()

                                    desafioFinded.item_desafiado = jogador_item
                                    desafioFinded.save()

                                    serializer = DesafioSerializer(desafioFinded)

                                    return Response(serializer.data, status=200)
                            else:
                                return Response({"error": True,
                                                 "message": "Esse item não pertence a esse jogador."},
                                                status=400)
                        else:
                            return Response({"error": True,
                                             "message": "Esse item não existe para esse jogador."},
                                            status=400)
                elif jogadorFinded == desafioFinded.desafiante:
                    if JogadorItem.objects.get(pk=int(desafio['item'])):
                        jogador_item = JogadorItem.objects.get(pk=int(desafio['item']))

                        if jogador_item.jogador == jogadorFinded:
                            if jogador_item.quantidade_bloqueada == jogador_item.quantidade:
                                return Response({"error": True,
                                                 "message": "Você esta com esse item bloqueado, ou seja, já esta usando em outro desafio."},
                                                status=400)
                            else:
                                jogador_item.quantidade_bloqueada = jogador_item.quantidade_bloqueada + 1
                                jogador_item.save()

                                jogador_item_old = JogadorItem.objects.get(pk=desafioFinded.item_desafiante.id)
                                jogador_item_old.quantidade_bloqueada = jogador_item_old.quantidade_bloqueada - 1
                                jogador_item_old.save()

                                desafioFinded.item_desafiante = jogador_item
                                desafioFinded.save()

                                serializer = DesafioSerializer(desafioFinded)

                                return Response(serializer.data, status=200)
                        else:
                            return Response({"error": True,
                                             "message": "Esse item não pertence a esse jogador."},
                                            status=400)
                    else:
                        return Response({"error": True,
                                         "message": "Esse item não existe para esse jogador."},
                                        status=400)

            else:
                return Response({"error": True, "message": "Você não é um jogador."}, status=400)
        else:
            return Response({"error": True, "message": "Desafio não existe."}, status=400)


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='listarDesafios')
    def ListarDesafios(self, request):
        jogadorFinded = Jogador.objects.get(user=request.user)
        desafios = Desafio.objects.filter(desafiante=jogadorFinded) | Desafio.objects.filter(desafiado=jogadorFinded)

        serializer = DesafioSerializer(desafios, many=True)

        return Response({'List': serializer.data})


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarDesafios')
    def ConsultarDesafios(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            desafio = jsonData
        else:
            desafio = request.POST.get('desafio', '')

        jogadorFinded = Jogador.objects.get(user=request.user)
        desafioFinded = Desafio.objects.get(pk=desafio['id'])

        if jogadorFinded == desafioFinded.desafiante or jogadorFinded == desafioFinded.desafiado:

            serializer = DesafioSerializer(desafioFinded)
            return Response({'Desafio': serializer.data})
        else:
            return Response({"error": True,
                             "message": "Esse desafio não pertence a você."},
                            status=400)