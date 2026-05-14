"""
URL configuration for projeto project.

The urlpatterns list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rotas do site
    path('', include('siteapp.urls')),

    # Painel admin
    path('admin/', admin.site.urls),

    # Rotas da API
    path('', include('core.urls')),
]