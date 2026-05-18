"""
URL configuration for projeto project.

The urlpatterns list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rotas da Interface do Site (Login, Home, Cadastro de Imóveis)
    path('', include('siteapp.urls')),

    # Painel Nativo de Administração do Django (Se necessário)
    path('django-admin/', admin.site.urls), # Mudado para evitar conflito com seu app

    # Rotas de Endpoints da API REST (Isoladas com o prefixo 'api/')
    path('api/', include('core.urls')),
    
]
