from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Importa todas as views do seu arquivo views.py (incluindo a função index)
from .views import * # 1. Configuração do Router para os ViewSets de Imóveis
router = DefaultRouter()
router.register(r'terrenos', viewset=TerrenoViewSet, basename='terreno')
router.register(r'casas', viewset=CasaViewSet, basename='casa')
router.register(r'salas-comerciais', viewset=SalaComercialViewSet, basename='salacomercial')
router.register(r'galpoes-comerciais', viewset=GalpaoComercialViewSet, basename='galpaocomercial')
router.register(r'sitios', viewset=SitioViewSet, basename='sitio')
router.register(r'chacaras', viewset=ChacaraViewSet, basename='chacara')
router.register(r'apartamentos', viewset=ApartamentoViewSet, basename='apartamento')
router.register(r'vendas', viewset=VendaViewSet)
router.register(r'fotos-imovel', viewset=FotosImovelViewSet)

urlpatterns = [   
    # Painel Administrativo
    path('admin/', admin.site.urls),

    # --- ROTA DO SITE (FRONT-END) ---
    # Quando você acessar http://127.0.0.1:8000/ ele chamara a função index
    path('', index, name='index'), 

    # --- ROTAS DA API (BACK-END / THUNDER CLIENT) ---
    # Todas as rotas do router agora precisam do prefixo api/
    path('api/', include(router.urls)),

    # Endpoints de Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoints de Usuários e Cadastros
    path('api/pessoa-fisica/', ListCreatePessoaFisica.as_view()),
    path('api/pessoa-juridica/', ListCreatePessoaJuridica.as_view()),
    path('api/usuarios/', ListAllUsers.as_view()),
    path('api/telefones/', ListCreateTelefone.as_view()),
    path('api/enderecos-usuario/', ListCreateEnderecoUsuario.as_view()),
]

# Configuração para exibir as fotos dos imóveis no navegador
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)