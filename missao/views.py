import base64
import imghdr
import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer

from missao.api.serializers import GrupoSerializer, MissaoSerializer
from missao.models import Grupo, Missao

class GrupoViewSet(GenericViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='listarGrupos')
    def ListarGrupos(self, request):
        grupos = Grupo.objects.all()
        serializer = GrupoSerializer(grupos, many=True)

        return Response({'List': serializer.data})

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='consultarGrupo/(?P<pk>[0-9]+)$') 
    def ConsultarGrupos(self, request, pk=None):
        grupo = Grupo.objects.get(id=pk)
        serializer = GrupoSerializer(grupo)

        return Response({'Grupo': serializer.data})
    
    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='missoes/(?P<pk>[0-9]+)$') 
    def missoes(self, request, pk=None):
        grupo = Grupo.objects.get(id=pk)
        missoes = Missao.objects.filter(id_milestone=grupo.id_milestone)
        print(missoes)
        serializer = MissaoSerializer(missoes, many=True)

        return Response({'Missoes': serializer.data})