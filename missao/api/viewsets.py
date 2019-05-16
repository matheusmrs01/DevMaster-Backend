from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

from jogador.models import Jogador
from missao.models import Missao
from django.contrib.auth.models import User

from .serializers import MissaoSerializer, CriarMissaoSerializer

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
        if request.user == missão.jogador.user:
            serializer = MissaoSerializer(missão)
            return Response(serializer.data)
        else:
            return Response({'Você não é o dono da missão!'})


    def update(self, request, pk, *args, **kwargs):
        missao = Missao.objects.get(id=pk)
        if missao.jogador.user == request.user:
            return super(MissaoViewSet, self).update(request, *args, **kwargs)
        else:
            return Response({'Você não é dono desta missão!'})


