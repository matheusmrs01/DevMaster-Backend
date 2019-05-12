from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

from jogador.models import Jogador, Missao
from django.contrib.auth.models import User
from .serializers import JogadorSerializer, UserSerializer, MissaoSerializer, CriarJogadorSerializer, \
    CriarMissaoSerializer


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


class CriarMissaoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Missao.objects.all()
    serializer_class = CriarMissaoSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MissaoViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Missao.objects.all()
    serializer_class = MissaoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk, *args, **kwargs):
        missão = Missao.objects.get(id=pk)
        if request.user == missão.jogador.user or request.user.is_superadmin:
            serializer = MissaoSerializer(missão)
            return Response(serializer.data)
        else:
            return Response({'Você não é o dono da missão!'})

    def update(self, request, pk, *args, **kwargs):
        missao = Missao.objects.get(id=pk)
        if missao.jogador.user == request.user or request.user.is_superadmin:
            return super(MissaoViewSet, self).update(request, *args, **kwargs)
        else:
            return Response({'Você não é dono desta missão!'})


