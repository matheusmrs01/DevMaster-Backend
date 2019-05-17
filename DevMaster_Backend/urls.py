"""DevMaster_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from jogador.api.viewsets import JogadorViewSet, JogadorCreateViewSet
from missao.api.viewsets import CriarMissaoViewSet, MissaoViewSet
from evento.views import ItemViewSet

router = routers.DefaultRouter()
router.register(r'jogador', JogadorViewSet)
router.register(r'criarjogador', JogadorCreateViewSet)
router.register(r'criarmissao', CriarMissaoViewSet)
router.register(r'missao', MissaoViewSet)
router.register(r'item/<pk:id>', ItemViewSet, base_name='item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_auth.urls')),
    path('admin/', admin.site.urls),
]
