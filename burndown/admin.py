from django.contrib import admin
from .models import Burndown, MissaoBurndown

# Register your models here.

admin.site.register(Burndown)
admin.site.register(MissaoBurndown)