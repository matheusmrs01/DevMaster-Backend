import base64
import imghdr
import json
import requests
from datetime import datetime
import time

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
from jogador.models import Jogador, XpEvento
from desafio.models import DesafioMissoes
from evento.models import Evento
from django.contrib.auth.models import User

class IssueGitlabViewSet(GenericViewSet):
    queryset = Missao.objects.all()
    serializer_class = MissaoSerializer

    @method_decorator(csrf_exempt)
    @action(methods=['POST'], detail=False, url_path='gitlabissue')
    def CriarMissao(self, request):
        gitlab_token = request.META['HTTP_X_GITLAB_TOKEN']
        if (request.META['CONTENT_TYPE'] == 'application/json'):
            jsonData = json.loads(request.body)

            issue = jsonData
        else:
            issue = request.POST.get('issue', '')
        print('ANTES DO PRINT DA ISSUE')
        print(issue)
        if gitlab_token == '8ae957d6f68f46055091ff319fa67b888e122a3a':
            if issue['object_kind'] == 'issue':
                if issue['assignees']:
                    userFinded = User.objects.filter(username=issue['assignees'][0]['username'])
                    if userFinded:
                        jogadorFinded = Jogador.objects.filter(user=User.objects.get(username=issue['assignees'][0]['username']))
                        #Função usada para criar uma missão
                        if jogadorFinded:
                            jogadorFinded = Jogador.objects.get(user=User.objects.get(username=issue['assignees'][0]['username']))
                            if issue['object_attributes']['action'] == 'open':
                                newMissao = Missao()
                                newMissao.jogador = jogadorFinded
                                newMissao.nome_missao = issue['object_attributes']['title']
                                newMissao.xp_missao = 80

                                if issue['object_attributes']['due_date']:
                                    newMissao.data = issue['object_attributes']['due_date']
                                
                                newMissao.id_issue = issue['object_attributes']['id']
                                newMissao.id_projeto = issue['object_attributes']['project_id']

                                if issue['object_attributes']['milestone_id']:
                                    newMissao.id_milestone = issue['object_attributes']['milestone_id']
                                    if not Grupo.objects.filter(id_milestone=issue['object_attributes']['milestone_id']):
                                        newGrupo = Grupo()
                                        newGrupo.name = 'Milestone ' + str(issue['object_attributes']['milestone_id'])
                                        newGrupo.id_milestone = issue['object_attributes']['milestone_id']
                                        newGrupo.xp_grupo = 10
                                        newGrupo.save()
                                    else:
                                        grupoFinded = Grupo.objects.get(id_milestone=issue['object_attributes']['milestone_id'])
                                        grupoFinded.xp_grupo = grupoFinded.xp_grupo + 10
                                        grupoFinded.save()

                                newMissao.save()
                                return Response({'Missão cadastrada com sucesso!'})
                            
                            #finaliza a missão ja criada
                            elif issue['object_attributes']['action'] == 'close':
                                missaoFinded = Missao.objects.filter(id_issue=issue['object_attributes']['id'])
                                if(missaoFinded):
                                    missaoFinded = Missao.objects.get(id_issue=issue['object_attributes']['id'])
                                    if missaoFinded.status == False:
                                        # r = requests.get('https://gitlab.com/api/v4/projects/'+str(issue['object_attributes']['project_id'])+'/issues/'+str(issue['object_attributes']['id'])+'?private_token='+str(jogadorFinded.private_token))
                                        # issue = r.json()
                                        xpMissao = 80

                                        missaoFinded.status = True
                                        missaoFinded.nice_data = True
                                        missaoFinded.nice_tempo = True

                                        #verifica a data da missão e a data que vai ser finalizada
                                        if issue['object_attributes']['due_date']:
                                            missaoFinded.data = issue['object_attributes']['due_date']
                                            if datetime.now() > datetime.strptime(issue['object_attributes']['due_date'].replace('-','/'), '%Y/%m/%d'):
                                                xpMissao = xpMissao - 20
                                                missaoFinded.nice_data = False
                                            else:
                                                missaoFinded.nice_data = True
                                        
                                        #verifica se foi fechada no tempo certo
                                        if issue['object_attributes']['time_estimate']:
                                            if not issue['object_attributes']['total_time_spent']:
                                                xpMissao = xpMissao - 50
                                                missaoFinded.nice_tempo = False
                                            else:
                                                if issue['object_attributes']['time_estimate'] < issue['object_attributes']['total_time_spent']:
                                                    xpMissao = xpMissao - 50
                                                    missaoFinded.nice_tempo = False
                                                else:
                                                    missaoFinded.nice_tempo = True

                                        #Verifica se tem evento, para poder atualizar o valor da xp
                                        eventosAtivo = Evento.objects.filter(is_active=True)    
                                        if eventosAtivo:
                                            for eventoAtivo in eventosAtivo:
                                                xpMissao = xpMissao * eventoAtivo.multiplicador_xp
                                                if XpEvento.objects.filter(jogador=jogadorFinded,evento=eventoAtivo):
                                                    xpEventoFinded = XpEvento.objects.get(jogador=jogadorFinded,evento=eventoAtivo)
                                                    xpEventoFinded.xp_evento = xpEventoFinded.xp_evento + xpMissao
                                                    xpEventoFinded.save()
                                                else:
                                                    newXpEvento = XpEvento()
                                                    newXpEvento.evento = eventoAtivo
                                                    newXpEvento.jogador = jogadorFinded
                                                    newXpEvento.xp_evento = xpMissao
                                                    newXpEvento.save()

                                        missaoFinded.xp_ganha = xpMissao

                                        #missao desafio - salva o valor em cada missão do desafio
                                        missoesDesafio = DesafioMissoes.objects.filter(missao=missaoFinded)
                                        if missoesDesafio:
                                            for missaoDesafio in missoesDesafio:
                                                missaoDesafio.xp_ganha = xpMissao
                                                missaoDesafio.save()

                                        jogadorFinded.xp_total = jogadorFinded.xp_total + xpMissao
                                        jogadorFinded.save()
                                        missaoFinded.save()
                                        return Response({'Missão finalizada com sucesso!'})
                                    else:
                                        return Response({'Missão já foi fechada.'})
                                else:
                                    return Response({'Missão nunca foi cadastrada na base de dados.'})
                        
                            #reabre a issue
                            elif issue['object_attributes']['action'] == 'reopen':
                                missaoFinded = Missao.objects.get(id_issue=issue['object_attributes']['id'])
                                missaoFinded.status = False
                                missaoFinded.xp_ganha = 0
                                missoeFinded.save()
                                return Response({'Missão reaberta com sucesso!'})
                            else:
                                return Response({'Issue não é de um timpo tratavel pelo endpoint.'})
                        else:
                            return Response({'Jogador dessa Issue não existe.'})
                    else:
                        return Response({'Usuario não existe.'})
                else:
                    return Response({'Essa issue não é tratavel pelo endpoint'})
            else:
                return Response({'O objeto em questão não é um issue.'})
        else:
            return Response({'Sem autorização.'})

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