from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.http import Http404

from .models import *
from .serializers import *

# lista todos os usarios (PEssoa Fisica e Pessoa Jurica, 
# mas sem suas informacoes especificas)
class ListAllUsers(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Lista ou cria pessoa fisica
class ListCreatePessoaFisica(ListCreateAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer
    
# Lista ou cria pessoa juridica
class ListCreatePessoaJuridica(ListCreateAPIView):
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer

# Lista todos os telefones dos usuarios (sem filtro)
# Registra os telefones de um usuario
class ListCreateTelefone(ListCreateAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer

# Lista todos os enderecos dos usuarios (sem filtro)
# Registra os enderecos de um usuario
class ListCreateEnderecoUsuario(ListCreateAPIView):
    queryset = EnderecoUsuario.objects.all()
    serializer_class = EnderecoUsuarioSerializer

# Imovel
class TerrenoViewSet(viewsets.ModelViewSet):
    queryset = Terreno.objects.all()
    serializer_class = TerrenoSerializer

class CasaViewSet(viewsets.ModelViewSet):
    queryset = Casa.objects.all()
    serializer_class = CasaSerializer

class ApartamentoViewSet(viewsets.ModelViewSet):
    queryset = DetalhesApartamento.objects.all()
    serializer_class = DetalhesApartamentoSerializer

class SalaComercialViewSet(viewsets.ModelViewSet):
    queryset = SalaComercial.objects.all()
    serializer_class = SalaComercialSerializer

class GalpaoComercialViewSet(viewsets.ModelViewSet):
    queryset = GalpaoComercial.objects.all()
    serializer_class = GalpaoComercialSerializer

class SitioViewSet(viewsets.ModelViewSet):
    queryset = Sitio.objects.all()
    serializer_class = SitioSerializer

class ChacaraViewSet(viewsets.ModelViewSet):
    queryset = Chacara.objects.all()
    serializer_class = ChacaraSerializer
    


    
    

        
