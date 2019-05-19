import json

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings

from jogador.models import Jogador, XpEvento
from missao.models import Missao
from django.contrib.auth.models import User

from evento.models import Evento

from desafio.models import DesafioMissoes

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
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            missao = jsonData
        else:
            missao = request.POST.get('desafio', '')

        missaoFinded = Missao.objects.get(id=pk)
        if missaoFinded.jogador.user == request.user:
            missaoFinded.status = True
            missaoFinded.nice_tempo = missao['nice_tempo']
            if missao['nice_tempo'] == False:
                missaoFinded.xp_missao = missao['xp_missao']

            aux_xp = 0

            if Evento.objects.filter(is_active=True):
                eventos = Evento.objects.filter(is_active=True)

                for evento in eventos:
                    aux_xp = aux_xp + (missaoFinded.xp_missao * evento.multiplicador_xp)

                    if XpEvento.objects.filter(evento=evento,jogador=missaoFinded.jogador):
                        xpEventoFinded = XpEvento.objects.get(evento=evento,jogador=missaoFinded.jogador)
                        xpEventoFinded.xp_evento = xpEventoFinded.xp_evento + (missaoFinded.xp_missao * evento.multiplicador_xp)
                        xpEventoFinded.save()
                    else:
                        newXpEvento = XpEvento()
                        newXpEvento.evento = evento
                        newXpEvento.jogador = missaoFinded.jogador
                        newXpEvento.xp_evento = missaoFinded.xp_missao * evento.multiplicador_xp
                        newXpEvento.save()

            else:
                aux_xp = aux_xp + missaoFinded.xp_missao

            if DesafioMissoes.objects.filter(missao=missaoFinded):
                desafioMissoesFinded = DesafioMissoes.objects.filter(missao=missaoFinded)

                for desafiomissaoFinded in desafioMissoesFinded:
                    auxDeMi = DesafioMissoes.objects.get(id=desafiomissaoFinded.id)
                    auxDeMi.xp_ganha = aux_xp
                    auxDeMi.save()

            missaoFinded.xp_ganha = aux_xp
            missaoFinded.save()

            serializer = MissaoSerializer(missaoFinded)
            return Response({'Missão atualizada com sucesso.'})
        else:
            return Response({'Você não é dono desta missão!'})


