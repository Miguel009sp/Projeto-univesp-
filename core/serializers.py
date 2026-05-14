from rest_framework import serializers
from django.db import transaction
from .models import (
    Usuario, PessoaFisica, PessoaJuridica, Telefone, EnderecoUsuario,
    Imovel, EnderecoImovel, FotosImovel, Terreno, Casa, Apartamento,
    DetalhesApartamento, SalaComercial, GalpaoComercial, Sitio, Chacara, Venda
)

# ==========================================
# 1. SERIALIZERS DE USUÁRIOS E CONFIGURAÇÃO
# ==========================================

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'password', 'email', 'role', 'foto']
        extra_kwargs = {'password': {'write_only': True}}
    
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


# ==========================================
# 2. SERIALIZERS DE SUPORTE AOS IMÓVEIS
# ==========================================

class FotosImovelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FotosImovel
        fields = '__all__'

class EnderecoImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoImovel
        fields = ['bairro', 'logradouro', 'numero', 'complemento', 'cep', 'localidade', 'sigla_federacao']


# ==========================================
# 3. SERIALIZER ESTRUTURAL PAI (IMOVEL)
# ==========================================

class ImovelSerializer(serializers.ModelSerializer):
    endereco = EnderecoImovelSerializer()
    
    # Campo virtual para receber múltiplos arquivos binários de imagem em lote
    galeria_fotos = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta: 
        model = Imovel
        fields = '__all__'

    def create(self, validated_data):
        endereco_data = validated_data.pop('endereco')
        fotos_data = validated_data.pop('galeria_fotos', [])
        
        # Atribui o proprietário logado automaticamente via contexto da requisição
        validated_data['user'] = self.context['request'].user

        with transaction.atomic():
            # Cria a instância correspondente do modelo filho dinamicamente
            imovel = self.Meta.model.objects.create(**validated_data)
            
            # Cria e vincula o endereço ao id gerado
            EnderecoImovel.objects.create(imovel=imovel, **endereco_data)
            
            # Percorre o lote guardando cada imagem na galeria
            for foto in fotos_data:
                FotosImovel.objects.create(imovel=imovel, caminho=foto)
                
        return imovel
    
    def update(self, instance, validated_data):
        endereco_dados = validated_data.pop('endereco', None)
        fotos_data = validated_data.pop('galeria_fotos', None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if endereco_dados:
                endereco = instance.endereco
                for attr, value in endereco_dados.items():
                    setattr(endereco, attr, value)
                endereco.save()
            
            if fotos_data:
                for foto in fotos_data:
                    FotosImovel.objects.create(imovel=instance, caminho=foto)
        
        return instance


# ==========================================
# 4. CLASSES FILHAS (HERDANÇA AUTOMÁTICA)
# ==========================================

class TerrenoSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = Terreno
        fields = '__all__'

class CasaSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = Casa
        fields = '__all__'
    
class ApartamentoSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = Apartamento
        fields = "__all__"

class DetalhesApartamentoSerializer(ApartamentoSerializer):
    class Meta(ApartamentoSerializer.Meta):
        model = DetalhesApartamento
        fields = '__all__'
    
class SalaComercialSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = SalaComercial
        fields = '__all__'

class GalpaoComercialSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = GalpaoComercial
        fields = '__all__'

class SitioSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = Sitio
        fields = '__all__'

class ChacaraSerializer(ImovelSerializer):
    class Meta(ImovelSerializer.Meta):
        model = Chacara
        fields = '__all__'


# ==========================================
# 5. HISTÓRICO DE VENDAS
# ==========================================

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'
