from django.contrib import admin
from .models import Desafio, DesafioMissoes
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Desafio)
admin.site.register(DesafioMissoes)
TokenAdmin.raw_id_fields = ('user',)
