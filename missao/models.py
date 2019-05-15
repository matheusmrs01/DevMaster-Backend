from django.db import models
from jogador.models import Jogador

# Create your models here.
class Missao(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='Jogador')
    nome_missao = models.CharField(blank=False, max_length=200)
    xp_missao = models.FloatField(blank=False)
    data = models.CharField(max_length=100, default='', blank=True)
    nice_tempo = models.BooleanField(default=False, blank=False)
    status = models.BooleanField(default=False, blank=False)
    id_issue = models.IntegerField(default=0, blank=False)
    id_projeto = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return 'Jogador: ' + self.jogador.user.get_full_name() + ' - Missão: ' + self.nome_missao

class MissãoGrupo(models.Model):
    missao = models.ForeignKey(Missao, on_delete=models.CASCADE, related_name='MissãoGrupo')
    name = models.CharField(blank=True, max_length=200)
    xp_missao = models.FloatField(blank=False)
    status = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return 'Missão: ' + self.missao.name + ' - Name: ' + self.name