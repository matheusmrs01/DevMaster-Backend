from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from jogador.models import Jogador, XpEvento, JogadorItem
from django.contrib.auth.models import User
from .serializers import JogadorSerializer, UserSerializer, CriarJogadorSerializer, XpEventoSerializer

from evento.models import Evento


class JogadorCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Jogador.objects.all()
    serializer_class = CriarJogadorSerializer

    def create(self, request, *args, **kwargs):
        return super(JogadorCreateViewSet, self).create(request, *args, **kwargs)


class JogadorViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # Apenas para SuperAdmin
    def list(self, request, *args, **kwargs):  # usado para obter toda a lista
        return super(JogadorViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        if request.user == user or request.user.is_superuser:
            jogador = Jogador.objects.get(user=user)
            serializer = JogadorSerializer(jogador)
            return Response(serializer.data)
        else:
            return Response({'Você não é o jogador requisitado!'})

    def update(self, request, pk, *args, **kwargs):
        jogador = Jogador.objects.get(id=pk)
        try:
            if jogador.user == request.user or request.user.is_superuser:
                return super(JogadorViewSet, self).update(request, *args, **kwargs)
            else:
                return Response({'Você não é o jogador!'})
        except:
            return Response({'Ocorreu um erro, atualize e tente de novo!'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class XpeventoViewSet(GenericViewSet):
    queryset = XpEvento.objects.all()
    serializer_class = XpEventoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarXpsEvento')
    def ConsultarXpsEvento(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            xpEvento = jsonData
        else:
            xpEvento = request.POST.get('desafio', '')

        if Evento.objects.get(id=xpEvento['id']):
            evento = Evento.objects.get(id=xpEvento['id'])
            if XpEvento.objects.filter(evento=evento):
                xpEventoFinded = XpEvento.objects.filter(evento=evento).order_by('-xp_evento')
                serializer = XpEventoSerializer(xpEventoFinded, many=True)

                return Response({'List': serializer.data})
            else:
                return Response({'XPevento não existe'})
        else:
            return Response({'Evento não existe.'})



