from django.db import models
from jogador.models import Jogador, JogadorItem
from evento.models import Item
from missao.models import Missao

# Create your models here.

class Desafio(models.Model):
    STATUS_CHOICES = (
        ('P', 'Proposta'),
        ('A', 'Aposta'),
        ('C', 'Conslusão'),
    )

    nome = models.CharField(max_length=200, verbose_name='Nome Desafio', blank=False)
    desafiante = models.ForeignKey(Jogador, blank=True, on_delete=models.PROTECT, related_name='Desafiante')
    desafiado = models.ForeignKey(Jogador, blank=True, null=True, on_delete=models.PROTECT, related_name='Desafiado')
    status = models.CharField(verbose_name='Status', max_length=1, choices=STATUS_CHOICES, default='P')
    item_desafiante = models.ForeignKey(JogadorItem, blank=True, on_delete=models.PROTECT, related_name='ItemDesafiante')
    item_desafiado = models.ForeignKey(JogadorItem, blank=True, null=True, on_delete=models.PROTECT, related_name='ItemDesafiado')

    def __str__(self):
        return 'Desafio: ' + self.nome + ' - Entre: ' + self.desafiante.user.get_full_name()

class DesafioMissoes(models.Model):
    desafio = models.ForeignKey(Desafio, blank=False, on_delete=models.PROTECT, related_name='Desafio')
    missao = models.ForeignKey(Missao, blank=False, on_delete=models.PROTECT, related_name='Missão')

    def __str__(self):
        return 'Desafio: ' + self.desafio.nome + ' - Entre: ' + self.desafio.desafiante.user.get_full_name()