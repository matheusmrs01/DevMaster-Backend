from django.contrib import admin
from .models import Evento, Item
from jogador.models import XpEvento
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Evento)
admin.site.register(Item)
admin.site.register(XpEvento)
TokenAdmin.raw_id_fields = ('user',)
