from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

router = DefaultRouter()
router.register(r'terrenos', viewset=TerrenoViewSet)
router.register(r'casas', viewset=CasaViewSet)
router.register(r'salas-comerciais', viewset=SalaComercialViewSet)
router.register(r'galpoes-comerciais', viewset=GalpaoComercialViewSet)
router.register(r'sitios', viewset=SitioViewSet)
router.register(r'chacaras', viewset=ChacaraViewSet)
router.register(r'apartamentos', viewset=ApartamentoViewSet)
router.register(r'vendas', viewset=VendaViewSet)
router.register(r'fotos-imovel', viewset=FotosImovelViewSet)

urlpatterns = [   
    path('', include(router.urls)),

    # jwt token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # usuario comum (sem admin) url (GET e POST)
    path('pessoa-fisica', ListCreatePessoaFisica.as_view()),
    path('pessoa-juridica', ListCreatePessoaJuridica.as_view()),

    # todos os usuarios (lista sem informacao de pessoa fisica ou juridica - GET)
    path('usuarios', ListAllUsers.as_view()),
    path('telefones', ListCreateTelefone.as_view()),
    path('enderecos-usuario', ListCreateEnderecoUsuario.as_view()),
]
