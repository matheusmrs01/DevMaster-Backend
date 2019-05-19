from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=200, blank=False)
    descricao = models.TextField(blank=True)
    url_image = models.TextField(default='https://www.mariowiki.com/images/thumb/a/a6/Super_Mushroom_Artwork_-_Super_Mario_3D_World.png/1200px-Super_Mushroom_Artwork_-_Super_Mario_3D_World.png')

    def __str__(self):
        return self.name

class Evento(models.Model):
    name = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=False)
    multiplicador_xp = models.FloatField(blank=True, default=1)
    data_inicio = models.DateTimeField(blank=False)
    data_final = models.DateTimeField(null=True, blank=True)
    is_finalized = models.BooleanField(blank=True, default=False)
    primeiro = models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item1')
    segundo = models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item2')
    terceiro = models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item3')
    quarto = models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item4')
    quinto =models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item5')
    sexto = models.ForeignKey(Item, blank=True, null=True, on_delete=models.PROTECT, related_name='Item6')

    def __str__(self):
        return 'Nome: ' + self.name
