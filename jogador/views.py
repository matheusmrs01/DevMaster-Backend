from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from jogador.api.serializers import JogadorItemSerializer

from jogador.models import JogadorItem, Jogador

# Create your views here.

class JogadorItemViewSet(GenericViewSet):
    queryset = JogadorItem.objects.all()
    serializer_class = JogadorItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(csrf_exempt)
    @action(methods=['GET'], detail=False, url_path='itens')
    def ListarDesafios(self, request):
        jogadorFinded = Jogador.objects.get(user=request.user)
        jogadorItens = JogadorItem.objects.filter(jogador=jogadorFinded)

        serializer = JogadorItemSerializer(jogadorItens, many=True)

        return Response({'List': serializer.data})
