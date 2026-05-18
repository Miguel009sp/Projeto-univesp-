from django.shortcuts import render # Import necessário para o HTML
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework import viewsets
from .models import *
from .serializers import *

# Função auxiliar para filtrar preços
def obter_preco_filtrado(request):
    valor_procurado = (
        request.query_params.get('valor_maximo') or 
        request.query_params.get('preco') or 
        request.query_params.get('valor') or
        request.GET.get('valor_maximo')
    )
    if valor_procurado:
        try:
            valor_limpo = str(valor_procurado).replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(valor_limpo)
        except ValueError:
            return None
    return None

# --- VIEWS DE USUÁRIOS ---
class ListAllUsers(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ListCreatePessoaFisica(ListCreateAPIView):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer
    
class ListCreatePessoaJuridica(ListCreateAPIView):
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer

class ListCreateTelefone(ListCreateAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer

class ListCreateEnderecoUsuario(ListCreateAPIView):
    queryset = EnderecoUsuario.objects.all()
    serializer_class = EnderecoUsuarioSerializer

# --- VIEWSETS DE IMÓVEIS ---
class FotosImovelViewSet(viewsets.ModelViewSet):
    queryset = FotosImovel.objects.all()
    serializer_class = FotosImovelSerializer

class TerrenoViewSet(viewsets.ModelViewSet):
    serializer_class = TerrenoSerializer
    def get_queryset(self):
        queryset = Terreno.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class CasaViewSet(viewsets.ModelViewSet):
    serializer_class = CasaSerializer
    def get_queryset(self):
        queryset = Casa.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class ApartamentoViewSet(viewsets.ModelViewSet):
    serializer_class = DetalhesApartamentoSerializer
    def get_queryset(self):
        queryset = DetalhesApartamento.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class SalaComercialViewSet(viewsets.ModelViewSet):
    serializer_class = SalaComercialSerializer
    def get_queryset(self):
        queryset = SalaComercial.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class GalpaoComercialViewSet(viewsets.ModelViewSet):
    serializer_class = GalpaoComercialSerializer
    def get_queryset(self):
        queryset = GalpaoComercial.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class SitioViewSet(viewsets.ModelViewSet):
    serializer_class = SitioSerializer
    def get_queryset(self):
        queryset = Sitio.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class ChacaraViewSet(viewsets.ModelViewSet):
    serializer_class = ChacaraSerializer
    def get_queryset(self):
        queryset = Chacara.objects.all()
        preco = obter_preco_filtrado(self.request)
        if preco:
            queryset = queryset.filter(valor_original__lte=preco)
            
        # Filtro por Número de Referência
        referencia = self.request.query_params.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
            
        return queryset

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

# --- FUNÇÃO PARA RENDERIZAR O SITE ---
def index(request):
    return render(request, 'core/index.html')