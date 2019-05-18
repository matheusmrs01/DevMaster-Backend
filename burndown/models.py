from django.db import models
from missao.models import Missao

# Create your models here.
class Burndown(models.Model):
    is_active = models.BooleanField(default=True)
    data_inicio = models.DateField(blank=False)
    data_termino = models.DateField(blank=True, null=True)
    quantidade_missao = models.IntegerField(blank=True, default=0)
    quantidade_queimada = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return 'Inicio: ' + str(self.data_inicio) + ' - Final: ' + str(self.data_termino) + ' - Ativo: ' + str(self.is_active)

class MissaoBurndown(models.Model):
    burndown = models.ForeignKey(Burndown, blank=False, on_delete=models.PROTECT, related_name='Burndown')
    missao = models.ForeignKey(Missao, blank=False, on_delete=models.PROTECT, related_name='MissaoBurndown')

    def __str__(self):
        return 'Burndown: de ' + self.burndown.data_inicio + ' - a ' + self.burndown.data_termino