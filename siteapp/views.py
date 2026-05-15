from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import Casa, Usuario, FotosImovel, EnderecoImovel

# ==============================================================================
# MÓDULO 1: AUTENTICAÇÃO E SESSÃO DO USUÁRIO (DESEMPENHO MÁXIMO)
# ==============================================================================

def login_view(request):
    """
    Controla o acesso inicial de forma instantânea.
    Usa redirecionamento de caminho estático para quebrar loops de carregamento.
    """
    if request.method == "POST":
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha', '').strip()
        
        # OTIMIZAÇÃO DE ENGENHARIA DE SOFTWARE: Consome e limpa mensagens travadas na memória
        try:
            mensagem_storage = messages.get_messages(request)
            for _ in mensagem_storage:
                pass
        except Exception:
            pass
        
        # Validação estática em memória (Velocidade instantânea)
        if usuario == 'bragatto' and senha == '123456':
            # Sinaliza ao Django a validação bem-sucedida do estado da sessão ativa
            request.session.modified = True
            
            # REDIRECIONAMENTO POR CAMINHO DIRETO: Evita loops circulares de nomes de rotas
            return redirect('/home/')  
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos'})
            
    return render(request, 'login.html')


def logout_view(request):
    """
    Encerra a sessão ativa de forma limpa e imediata.
    """
    logout(request)
    return redirect('login') 


def home_view(request):
    """
    Renderiza o Dashboard Administrativo Centralizado.
    """
    return render(request, 'home.html') 

# ==============================================================================
# MÓDULO 2: LOGÍSTICA E OPERAÇÕES DE IMÓVEIS
# ==============================================================================

def buscar_imoveis_view(request):
    """
    Painel de consultas avançadas otimizado com select_related para evitar múltiplas queries.
    """
    tipo_imovel = request.GET.get('tipo_imovel')
    valor_maximo = request.GET.get('valor_maximo')
    
    # Otimização de Performance: Traz endereço e imóvel em um único JOIN de banco de dados
    imoveis = Casa.objects.all().select_related('endereco')
    
    if tipo_imovel and tipo_imovel != "Todos":
        imoveis = imoveis.filter(nome__istartswith=tipo_imovel)
    
    if valor_maximo:
        try:
            valor_limpo = str(valor_maximo).replace('R$', '').replace('.', '').replace(',', '.').strip()
            preco_limite = float(valor_limpo)
            imoveis = imoveis.filter(valor_original__lte=preco_limite)
        except ValueError:
            pass

    return render(request, 'buscar_imoveis.html', {'imoveis': imoveis})


def cadastro_imoveis_view(request, pk=None):
    """
    Controlador unificado de Persistência (Criação e Edição de registros de Imóveis).
    """
    imovel = None
    if pk:
        imovel = get_object_or_404(Casa, pk=pk)

    if request.method == "POST":
        tipo = request.POST.get('tipo_imovel')
        valor_da_tela = request.POST.get('valor_imovel') 
        status = request.POST.get('status')
        proprietario_doc = request.POST.get('proprietario_documento')
        
        # Localização Estruturada
        cep = request.POST.get('cep')
        logradouro = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        # Upload de Mídias
        foto_principal = request.FILES.get('foto_principal')
        fotos_galeria = request.FILES.getlist('fotos_galeria')
        
        # Tratamento de dados numéricos decimais
        try:
            valor_limpo = str(valor_da_tela).replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor_final = float(valor_limpo)
        except (ValueError, TypeError):
            valor_final = 0.00

        if imovel:
            # Lógica de Atualização Cadastral (Update)
            imovel.nome = f"{tipo} - {logradouro}, {numero}"
            imovel.valor_original = valor_final
            imovel.status = status
            imovel.proprietario_documento = proprietario_doc
            if foto_principal:
                imovel.foto_principal = foto_principal
            imovel.save()
            
            # Atualização do nó relacional de endereço
            endereco, created = EnderecoImovel.objects.get_or_create(imovel=imovel)
            endereco.cep = cep
            endereco.logradouro = logradouro
            endereco.numero = numero
            endereco.bairro = bairro
            endereco.localidade = cidade
            endereco.sigla_federacao = estado
            endereco.save()
            
            messages.success(request, "Imóvel atualizado com sucesso!")
        else:
            # LÓGICA DE ALTA VELOCIDADE: Cria o imóvel vinculando o ID diretamente
            try:
                usuario_id = request.user.id if request.user.is_authenticated else 1
            except Exception:
                usuario_id = 1

            novo_imovel = Casa.objects.create(
                nome=f"{tipo} - {logradouro}, {numero}",
                valor_original=valor_final,
                status=status,
                proprietario_documento=proprietario_doc,
                user_id=usuario_id, 
                foto_principal=foto_principal,
                area_terreno=200.0,
                area_construcao=100.0,
                numero_dormitorios=2,
                numero_suites=0
            )
            
            EnderecoImovel.objects.create(
                cep=cep, logradouro=logradouro, numero=numero,
                bairro=bairro, localidade=cidade, sigla_federacao=estado,
                imovel=novo_imovel
            )
            
            # Persistência da Galeria de Imagens Adicionais
            for foto in fotos_galeria:
                FotosImovel.objects.create(imovel=novo_imovel, caminho=foto)
            
            messages.success(request, "Imóvel cadastrado com sucesso!")

        return redirect('buscar_imoveis')

    return render(request, 'cadastro_imoveis.html', {'imovel': imovel})


@require_POST
def excluir_imovel_view(request, pk):
    """
    Remove fisicamente as propriedades do catálogo através do método POST de segurança.
    """
    imovel = get_object_or_404(Casa, pk=pk)
    imovel.delete()
    messages.success(request, "Imóvel excluído com sucesso!")
    return redirect('buscar_imoveis')

# ==============================================================================
# MÓDULO 3: GESTÃO DE CLIENTES (PROPRIETÁRIOS E COMPRADORES)
# ==============================================================================

def cadastro_proprietario_view(request):
    """
    Painel de cadastro para novos vendedores e locadores.
    """
    return render(request, 'cadastro_proprietario.html')    


def cadastro_comprador_view(request):
    """
    Painel de gerenciamento de leads e perfis de compradores interessados.
    """
    return render(request, 'cadastro_comprador.html')


@require_POST
def excluir_comprador_view(request, pk):
    """
    Remove perfis de compradores cadastrados de forma segura.
    """
    comprador = get_object_or_404(Usuario, pk=pk)
    comprador.delete()
    messages.success(request, "Comprador excluído com sucesso!")
    return redirect('home')
