from django.db import models
from missao.models import Missao

# Create your models here.
class Burndown(models.Model):
    is_active = models.BooleanField(default=True)
    data_inicio = models.DateField(blank=False)
    data_termino = models.DateField(blank=True, null=True)
    quantidade_missao = models.IntegerField(verbose_name='Quantidade de missões da semana', blank=True, default=0)
    quantidade_missao_falta = models.IntegerField(verbose_name='Quantidade de missões da semana passada, não queimadas', blank=True, null=True, default=None)
    quantidade_queimada_dia1 = models.IntegerField(blank=True, null=True, default=None)
    quantidade_queimada_dia2 = models.IntegerField(blank=True, null=True, default=None)
    quantidade_queimada_dia3 = models.IntegerField(blank=True, null=True, default=None)
    quantidade_queimada_dia4 = models.IntegerField(blank=True, null=True, default=None)
    quantidade_queimada_dia5 = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return 'Inicio: ' + str(self.data_inicio) + ' - Final: ' + str(self.data_termino) + ' - Ativo: ' + str(self.is_active)
