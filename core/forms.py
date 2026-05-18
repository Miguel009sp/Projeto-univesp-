from django import forms
from .models import (
    EnderecoImovel, FotosImovel, Terreno, Casa, 
    Apartamento, DetalhesApartamento, SalaComercial, 
    GalpaoComercial, Sitio, Chacara
)

# --- CAMPOS COMPARTILHADOS (HERDADOS DE IMOVEL) ---
# Lista de campos padrão que todo imóvel possui para evitar repetição de código
# ADICIONADOS: 'referencia' e 'proprietario_documento' para alinhar com o Model e o HTML
CAMPOS_BASE_IMOVEL = [
    'nome', 
    'referencia', 
    'descricao', 
    'foto_principal', 
    'proprietario_documento', 
    'valor_original', 
    'status'
]


# --- FORMULÁRIO DE ENDEREÇO ---
class EnderecoImovelForm(forms.ModelForm):
    class Meta:
        model = EnderecoImovel
        fields = ['cep', 'logradouro', 'numero', 'bairro', 'complemento', 'localidade', 'sigla_federacao']


# --- FORMULÁRIO DE FOTOS (GALERIA) ---
class FotosImovelForm(forms.ModelForm):
    class Meta:
        model = FotosImovel
        fields = ['caminho']
        widgets = {
            # Permite a seleção de múltiplos arquivos de imagem simultaneamente
            'caminho': forms.ClearableFileInput(attrs={'multiple': True}),
        }


# --- FORMULÁRIOS ESPECÍFICOS POR TIPO DE IMÓVEL ---

class TerrenoForm(forms.ModelForm):
    class Meta:
        model = Terreno
        fields = CAMPOS_BASE_IMOVEL + ['metragem']


class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = CAMPOS_BASE_IMOVEL + ['area_terreno', 'area_construcao', 'numero_dormitorios', 'numero_suites']


class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = CAMPOS_BASE_IMOVEL + ['area_util', 'numero_dormitorios', 'numero_suites']


class DetalhesApartamentoForm(forms.ModelForm):
    class Meta:
        model = DetalhesApartamento
        # Como herda de Apartamento, inclui os campos da base, do apartamento e os específicos de detalhes
        fields = CAMPOS_BASE_IMOVEL + ['area_util', 'numero_dormitorios', 'numero_suites', 'bloco', 'andar']


class SalaComercialForm(forms.ModelForm):
    class Meta:
        model = SalaComercial
        fields = CAMPOS_BASE_IMOVEL + ['area_util']


class GalpaoComercialForm(forms.ModelForm):
    class Meta:
        model = GalpaoComercial
        fields = CAMPOS_BASE_IMOVEL + ['area_util']


class SitioForm(forms.ModelForm):
    class Meta:
        model = Sitio
        fields = CAMPOS_BASE_IMOVEL + ['area_total', 'benfeitorias']


class ChacaraForm(forms.ModelForm):
    class Meta:
        model = Chacara
        fields = CAMPOS_BASE_IMOVEL + ['area_total', 'area_construida', 'numero_casas']