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

class EnderecoImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoImovel
        fields = ['bairro', 'logradouro', 'numero', 'complemento', 'cep', 'localidade', 'sigla_federacao']

class ImovelSerializer(serializers.ModelSerializer):

    endereco = EnderecoImovelSerializer()

    class Meta: 
        model = Imovel
        fields = '__all__'

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        imovel = self.Meta.model.objects.create(**validated_data)
        EnderecoImovel.objects.create(imovel=imovel, **endereco_data)
        return imovel
    
    def update(self, instance, validated_data):
        endereco_dados = validated_data.pop('endereco')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if endereco_dados:
            endereco = instance.endereco
            for attr, value in endereco_dados.items():
                setattr(endereco, attr, value)
            endereco.save()
        
        return instance


class TerrenoSerializer(ImovelSerializer):
    class Meta:
        model = Terreno
        fields = '__all__'

class CasaSerializer(ImovelSerializer):
    class Meta:
        model = Casa
        fields = '__all__'
    
class ApartamentoSerializer(ImovelSerializer):
    class Meta:
        model = Apartamento
        fields = "__all__"

class DetalhesApartamentoSerializer(ApartamentoSerializer):
    class Meta:
        model = DetalhesApartamento
        fields = '__all__'
    
class SalaComercialSerializer(ImovelSerializer):
    class Meta:
        model = SalaComercial
        fields = '__all__'

class GalpaoComercialSerializer(ImovelSerializer):
    class Meta:
        model = GalpaoComercial
        fields = '__all__'

class SitioSerializer(ImovelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'

class ChacaraSerializer(ImovelSerializer):
    class Meta:
        model = Chacara
        fields = '__all__'

# venda
class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

        