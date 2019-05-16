from django.contrib import admin
from .models import Missao, MissãoGrupo
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Missao)
admin.site.register(MissãoGrupo)
TokenAdmin.raw_id_fields = ('user',)