from django.contrib import admin
from .models import Jogador, Missao
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Jogador)
admin.site.register(Missao)
TokenAdmin.raw_id_fields = ('user',)
