import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from burndown.serializers import BurndownSerializer, MissaoBurndownSerializer
from .models import Burndown, MissaoBurndown


class BurndownViewSet(GenericViewSet):
    queryset = Burndown.objects.all()
    serializer_class = BurndownSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='AtualizarBurndown')
    def atualizarBurndown(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            burndown = jsonData
        else:
            burndown = request.POST.get('burndown', '')

        burndownFinded = Burndown.objects.get(pk=burndown['id'])
        missoesBurndown = MissaoBurndown.objects.filter(burndown=burndownFinded)

        if missoesBurndown:
            auxM = 0
            auxMF = 0
            for missaoBurndown in missoesBurndown:
                auxM = auxM + 1
                if missaoBurndown.missao.status:
                    auxMF = auxMF + 1

            burndownFinded.quantidade_missao = auxM
            burndownFinded.quantidade_queimada = auxMF
            burndownFinded.save()

            return Response({"message": "Burndown Atualizado."})
        else:
            return Response({"message": "Esse Burndown não tem missões."})


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='ListarBurndown')
    def listarBurndown(self, request):
        burndowns = Burndown.objects.all().order_by('-data_inicio')
        serializer = BurndownSerializer(burndowns, many=True)

        return Response({'List': serializer.data})


    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='ConsultarBurndown/(?P<pk>[0-9]+)$')
    def consultarBurndown(self, request, pk=None):

        burndownFinded = Burndown.objects.get(pk=pk)
        serializer = BurndownSerializer(burndownFinded)

        return Response({'Burndown': serializer.data})

class MissaoBurndownViewSet(GenericViewSet):
    queryset = MissaoBurndown.objects.all()
    serializer_class = MissaoBurndownSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='ListarMissaoBurndown')
    def listarMissãoBurndown(self, request):
        missaoburndowns = MissaoBurndown.objects.all()
        serializer = MissaoBurndownSerializer(missaoburndowns, many=True)

        return Response({'List': serializer.data})

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='ConsultarMissaoBurndown')
    def consultarMissaoBurndown(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            burndown = jsonData
        else:
            burndown = request.POST.get('burndown', '')

        missaoburndownFinded = MissaoBurndown.objects.get(pk=burndown['id'])
        serializer = MissaoBurndownSerializer(missaoburndownFinded)

        return Response({'MissaoBurndown': serializer.data})