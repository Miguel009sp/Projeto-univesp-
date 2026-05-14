from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, PessoaFisica, PessoaJuridica, Telefone, EnderecoUsuario,
    Imovel, EnderecoImovel, FotosImovel, Terreno, Casa, Apartamento,
    DetalhesApartamento, SalaComercial, GalpaoComercial, Sitio, Chacara, Venda
)

# 1. Configurações inline (permitem cadastrar tudo na mesma página do imóvel)
class FotosImovelInline(admin.TabularInline):
    model = FotosImovel
    fk_name = 'imovel'  # Especifica a chave estrangeira correta do seu models.py
    extra = 3  # Quantidade de campos vazios para fotos adicionais por padrão

class EnderecoImovelInline(admin.StackedInline):
    model = EnderecoImovel
    can_delete = False

# 2. Configuração do Admin do Usuário Customizado e seus tipos
class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1

class EnderecoUsuarioInline(admin.StackedInline):
    model = EnderecoUsuario
    extra = 1

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Reaproveita os campos padrões do Django UserAdmin e adiciona os seus customizados
    fieldsets = UserAdmin.fieldsets + (
        ('Informações de Perfil', {'fields': ('nome', 'foto', 'role')}),
    )
    list_display = ('username', 'email', 'nome', 'role', 'is_staff')

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('username', 'nome', 'cpf')
    inlines = [TelefoneInline, EnderecoUsuarioInline]

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('username', 'nome_empresa', 'cnpj')
    inlines = [TelefoneInline, EnderecoUsuarioInline]

# 3. Configuração do Admin de Imóveis (Base e Heranças)
# Todos os tipos abaixo herdarão a capacidade de cadastrar endereço e fotos juntos
@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user', 'valor_original', 'status')
    list_filter = ('status',)
    search_fields = ('nome', 'descricao')
    inlines = [EnderecoImovelInline, FotosImovelInline]

@admin.register(Casa)
class CasaAdmin(ImovelAdmin):
    pass

@admin.register(Apartamento)
class ApartamentoAdmin(ImovelAdmin):
    pass

@admin.register(DetalhesApartamento)
class DetalhesApartamentoAdmin(ImovelAdmin):
    pass

@admin.register(Terreno)
class TerrenoAdmin(ImovelAdmin):
    pass

@admin.register(SalaComercial)
class SalaComercialAdmin(ImovelAdmin):
    pass

@admin.register(GalpaoComercial)
class GalpaoComercialAdmin(ImovelAdmin):
    pass

@admin.register(Sitio)
class SitioAdmin(ImovelAdmin):
    pass

@admin.register(Chacara)
class ChacaraAdmin(ImovelAdmin):
    pass

# 4. Histórico de Vendas
@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'comprador', 'vendedor', 'preco_final', 'status', 'data_fechamento')
    list_filter = ('status', 'data_publicacao')

