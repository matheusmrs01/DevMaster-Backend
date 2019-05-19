from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Jogador(models.Model):
    """Essa classe se destina para o cadastro de Jogador"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Jogador', blank = True)
    xp_total = models.FloatField(default=0, blank=True)
    m_realizadas = models.IntegerField(default=0, blank=True)
    m_adquiridas = models.IntegerField(default=0, blank=True)
    mr_nadata = models.IntegerField(default=0, blank=True)
    private_token = models.CharField(blank=False, max_length=100)
    url_imagem = models.CharField(blank=False, max_length=300, default='')

    def __str__(self):
        return 'Jogador: %s' % (self.user.get_full_name())

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