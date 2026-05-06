from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = fields = ['username', 'nome', 'password', 'email', 'role', 'foto']
        extra_kwargs = {'password': {'write_only': True}}
    
# usuarios com role CUSTOMER. Depois vou fazer o especifico
# p/ admin
class PessoaFisicaSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta):
        model = PessoaFisica
        fields = UsuarioSerializer.Meta.fields + ['cpf', 'rg']

    def create(self, validated_data):
        user = PessoaFisica.objects.create_user(**validated_data)
        return user
    
class PessoaJuridicaSerializer(UsuarioSerializer):
    class Meta(UsuarioSerializer.Meta): 
        model = PessoaJuridica
        fields = UsuarioSerializer.Meta.fields + ['cnpj', 'nome_empresa', 'nome_comercial']

    def create(self, validated_data):
        user = PessoaJuridica.objects.create_user(**validated_data)
        return user
    
class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = '__all__'

class EnderecoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoUsuario
        fields = '__all__'
    

# Imoveis
class FotosImovelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FotosImovel
        fields = '__all__'

class ImovelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Imovel
        fields = '__all__'

class TerrenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terreno
        fields = "__all__"

class CasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casa
        fields = '__all__'
    
class ApartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartamento
        fields = "__all__"

class DetalhesApartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalhesApartamento
        fields = '__all__'
    
class SalaComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaComercial
        fields = '__all__'

class GalpaoComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalpaoComercial
        fields = '__all__'

class SitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'

class ChacaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chacara
        fields = '__all__'

        