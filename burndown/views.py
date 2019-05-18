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
    @action(methods=['GET'], detail=False, url_path='ListarBurndown')
    def listarBurndown(self, request):
        burndowns = Burndown.objects.all()
        serializer = BurndownSerializer(burndowns, many=True)

        return Response({'List': serializer.data})

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='ConsultarBurndown')
    def consultarBurndown(self, request):
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            burndown = jsonData
        else:
            burndown = request.POST.get('desafio', '')

        burndownFinded = Burndown.objects.get(pk=burndown['id'])
        serializer = BurndownSerializer(burndownFinded)

        return Response({'Burndown': serializer.data})