from django.db import models
from jogador.models import Jogador

# Create your models here.
class Missao(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='Jogador')
    nome_missao = models.CharField(blank=False, max_length=200)
    xp_ganha = models.FloatField(blank=True, default=0)
    xp_missao = models.FloatField(blank=False)
    data = models.CharField(max_length=100, default='', blank=True)
    nice_tempo = models.BooleanField(default=False, blank=False)
    nice_data = models.BooleanField(default=False, blank=False)
    status = models.BooleanField(default=False, blank=False)
    id_issue = models.IntegerField(default=0, blank=False)
    id_projeto = models.IntegerField(default=0, blank=False)
    id_milestone = models.IntegerField(default=None, null=True, blank=True) 

    def __str__(self):
        return 'Jogador: ' + self.jogador.user.get_full_name() + ' - Missão: ' + self.nome_missao

class Grupo(models.Model):
    name = models.CharField(blank=True, max_length=200)
    xp_grupo = models.FloatField(blank=False)
    status = models.BooleanField(default=False, blank=False)
    id_milestone = models.IntegerField(default=0, blank=False) 
    participantes = models.CharField(max_length=500, default='jogador', blank=False)

    def __str__(self):
        return 'Missão: ' + self.name + ' - xp_grupo: ' + str(self.xp_grupo)